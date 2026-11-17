import type { CapacitorConfig } from '@capacitor/cli';

// The apps are a native shell around the live Django site, so every change you deploy shows up in
// both apps right away. Only changes to this folder (plugins, icons, this file) need a new store build.
//
// SITE_URL picks the site the apps load:
//   production:        set PRODUCTION_URL below once the site is hosted
//   Android emulator:  SITE_URL=http://10.0.2.2:8000 npx cap run android   (10.0.2.2 is your PC)
//   phone on Wi-Fi:    SITE_URL=http://<your PC's LAN IP>:8000 npx cap run android
const PRODUCTION_URL = 'https://REPLACE-WITH-YOUR-SITE.example'; // TODO: your hosted site, e.g. https://yourname.pythonanywhere.com
const siteUrl = process.env.SITE_URL || PRODUCTION_URL;

const config: CapacitorConfig = {
  appId: 'com.thekinkylist.app',
  appName: 'The Kinky List',
  webDir: 'www',
  backgroundColor: '#16050f',
  server: {
    url: siteUrl,
    // Plain http is only allowed for local testing; the stores need https.
    cleartext: siteUrl.startsWith('http://'),
    androidScheme: 'https',
  },
  android: {
    // Lets you inspect the app in chrome://inspect during development.
    webContentsDebuggingEnabled: siteUrl !== PRODUCTION_URL,
  },
  ios: {
    contentInset: 'never',
  },
  experimental: {
    ios: {
      spm: {
        // Required by @capacitor-firebase/messaging to avoid a Swift package name clash with Firebase.
        packageOptions: {
          '@capacitor-firebase/messaging': { symlink: true },
        },
      },
    },
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1200,
      launchAutoHide: true,
      backgroundColor: '#16050f',
      showSpinner: false,
    },
    // Capacitor's built-in system bars: light icons for the dark site, whatever the phone's theme.
    SystemBars: {
      style: 'DARK',
    },
    // Push notifications. iOS: also show them while the app is open.
    FirebaseMessaging: {
      presentationOptions: ['alert', 'badge', 'sound'],
    },
    StatusBar: {
      style: 'DARK',
      backgroundColor: '#3b0a24',
      overlaysWebView: false,
    },
  },
};

export default config;
