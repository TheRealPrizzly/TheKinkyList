from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from assignments.models import Assignment, Reply
from games.registry import GAMES
from games.services import create_assignments
from kinkylist.test_utils import make_items, make_space, make_user

from . import fcm
from .models import Device

PUSH_ON = override_settings(FCM_SERVICE_ACCOUNT_FILE="test-service-account.json")


def add_device(user, token):
    return Device.objects.create(user=user, token=token, platform=Device.ANDROID)


class RegisterDeviceTests(TestCase):
    def setUp(self):
        self.a = make_user("a")
        self.client.force_login(self.a)
        self.url = reverse("push:register_device")

    def test_registers_and_remembers_token_in_session(self):
        response = self.client.post(self.url, {"token": "tok-1", "platform": "android"})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Device.objects.get().user, self.a)
        self.assertEqual(self.client.session["push_token"], "tok-1")

    def test_token_moves_to_whoever_is_logged_in(self):
        add_device(make_user("b"), "shared-phone")
        self.client.post(self.url, {"token": "shared-phone", "platform": "ios"})
        device = Device.objects.get()
        self.assertEqual((device.user, device.platform), (self.a, Device.IOS))

    def test_rejects_bad_input(self):
        for data in [{}, {"token": "t", "platform": "windows"}, {"token": "x" * 300, "platform": "android"}]:
            self.assertEqual(self.client.post(self.url, data).status_code, 400, data)
        self.assertFalse(Device.objects.exists())

    def test_requires_login_and_post(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url, {"token": "t", "platform": "android"}).status_code, 302)

    def test_logout_forgets_only_this_phone(self):
        add_device(self.a, "other-phone")
        self.client.post(self.url, {"token": "this-phone", "platform": "android"})
        self.client.post(reverse("logout"))
        self.assertEqual(list(Device.objects.values_list("token", flat=True)), ["other-phone"])

    def test_deleting_account_removes_devices(self):
        add_device(self.a, "tok")
        self.client.post(reverse("delete_account"), {"password": "pw-for-tests-123"})
        self.assertFalse(Device.objects.exists())


@PUSH_ON
@mock.patch("push.fcm.send")
class NotificationTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Sam")
        self.space = make_space(self.a, self.b)
        self.item = make_items(self.space, "Candlelit bath")[0]
        add_device(self.a, "a-phone")
        add_device(self.b, "b-phone")

    def sent(self, send):
        return [(c.args[0], c.args[2]) for c in send.call_args_list]

    def draw(self, drawer, *assignees, items=None):
        items = items or [self.item]
        with self.captureOnCommitCallbacks(execute=True):
            create_assignments(
                self.space, GAMES["randomize"], drawer, items, {i.id: [u.id for u in assignees] for i in items}
            )
        return Assignment.objects.filter(item__in=items).first()

    def test_drawing_notifies_assignees_discreetly(self, send):
        self.draw(self.a, self.a, self.b)
        self.assertEqual(self.sent(send), [("b-phone", "Alex drew something for you 💌")])
        self.assertEqual(send.call_args.args[3], reverse("assignments:list", args=[self.space.id]))

    def test_drawing_several_counts_them(self, send):
        items = [self.item, *make_items(self.space, "Dance")]
        self.draw(self.a, self.b, items=items)
        self.assertEqual(self.sent(send), [("b-phone", "Alex drew 2 wishes for you 💌")])

    def test_previews_name_the_wish(self, send):
        self.b.profile.notification_previews = True
        self.b.profile.save()
        self.draw(self.a, self.b)
        self.assertEqual(self.sent(send), [("b-phone", "Alex drew “Candlelit bath” for you.")])

    def test_drawing_for_yourself_sends_nothing(self, send):
        self.draw(self.a, self.a)
        send.assert_not_called()

    def test_reply_notifies_whoever_drew_it(self, send):
        assignment = self.draw(self.a, self.b)
        send.reset_mock()
        self.client.force_login(self.b)
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(
                reverse("assignments:reply", args=[self.space.id, assignment.id]), {"kind": Reply.NOT_FOR_ME}
            )
        self.assertEqual(self.sent(send), [("a-phone", "Sam answered a wish you drew.")])

    def test_reply_preview_says_how(self, send):
        self.a.profile.notification_previews = True
        self.a.profile.save()
        assignment = self.draw(self.a, self.b)
        send.reset_mock()
        self.client.force_login(self.b)
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(
                reverse("assignments:reply", args=[self.space.id, assignment.id]), {"kind": Reply.INTERESTED}
            )
        self.assertEqual(self.sent(send), [("a-phone", "Sam is interested in “Candlelit bath”.")])

    def test_completing_notifies_everyone_else_on_it(self, send):
        c = make_user("c", "Kim")
        self.space.memberships.create(user=c)
        add_device(c, "c-phone")
        assignment = self.draw(self.a, self.b, c)
        send.reset_mock()
        self.client.force_login(self.b)
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("assignments:complete", args=[self.space.id, assignment.id]))
        self.assertEqual(
            sorted(self.sent(send)),
            [("a-phone", "Sam checked something off your list."), ("c-phone", "Sam checked something off your list.")],
        )

    def test_joining_notifies_members(self, send):
        c = make_user("c", "Kim")
        self.client.force_login(c)
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("spaces:join"), {"code": self.space.invite_code})
            # Joining again changes nothing and sends nothing more.
            self.client.post(reverse("spaces:join"), {"code": self.space.invite_code})
        self.assertEqual(
            sorted(self.sent(send)), [("a-phone", "Kim joined your space."), ("b-phone", "Kim joined your space.")]
        )

    def test_gone_device_is_forgotten(self, send):
        send.side_effect = fcm.InvalidToken("b-phone")
        self.draw(self.a, self.b)
        self.assertFalse(Device.objects.filter(token="b-phone").exists())

    def test_failures_never_reach_the_user(self, send):
        send.side_effect = RuntimeError("Firebase is down")
        with self.assertLogs("push.notify", "ERROR"):
            self.draw(self.a, self.b)
        self.assertEqual(Assignment.objects.count(), 1)

    @override_settings(FCM_SERVICE_ACCOUNT_FILE="")
    def test_nothing_sent_when_push_is_off(self, send):
        self.draw(self.a, self.b)
        send.assert_not_called()


class FcmTests(TestCase):
    def test_message_carries_url_and_android_icon(self):
        message = fcm.build_message("tok", "Title", "Body", "/s/1/assignments/")
        self.assertEqual(message["data"], {"url": "/s/1/assignments/"})
        self.assertEqual(message["notification"], {"title": "Title", "body": "Body"})
        self.assertEqual(message["android"]["notification"]["icon"], "ic_stat_heart")

    def fake_session(self, status, payload):
        response = mock.Mock(ok=200 <= status < 300, status_code=status, text=str(payload))
        response.json.return_value = payload
        session = mock.Mock()
        session.credentials.project_id = "kinky"
        session.post.return_value = response
        return session

    def test_unregistered_token_raises(self):
        payload = {"error": {"details": [{"errorCode": "UNREGISTERED"}]}}
        with mock.patch("push.fcm._authorized_session", return_value=self.fake_session(404, payload)):
            with self.assertRaises(fcm.InvalidToken):
                fcm.send("tok", "t", "b", "/")

    def test_other_errors_are_logged(self):
        payload = {"error": {"details": [{"errorCode": "QUOTA_EXCEEDED"}]}}
        session = self.fake_session(429, payload)
        with mock.patch("push.fcm._authorized_session", return_value=session):
            with self.assertLogs("push.fcm", "WARNING"):
                fcm.send("tok", "t", "b", "/")
        self.assertIn("projects/kinky/messages:send", session.post.call_args.args[0])


class TemplateTests(TestCase):
    def setUp(self):
        self.a = make_user("a")
        self.space = make_space(self.a)
        self.client.force_login(self.a)
        self.dashboard = reverse("spaces:dashboard", args=[self.space.id])

    def test_push_script_and_prompt_only_when_push_is_on(self):
        response = self.client.get(self.dashboard)
        self.assertNotContains(response, "js/push.js")
        self.assertNotContains(response, "data-push-prompt")
        with PUSH_ON:
            response = self.client.get(self.dashboard)
        self.assertContains(response, "js/push.js")
        self.assertContains(response, "data-push-prompt")

    def test_profile_has_preview_switch(self):
        self.assertContains(self.client.get(reverse("profile")), "Show wish titles in notifications")
