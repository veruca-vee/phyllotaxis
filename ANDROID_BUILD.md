# Android APK Build Instructions

> **Note**: The Android SDK is not available in the sandbox environment, so the APK cannot be built here. However, all the necessary files are configured and ready for you to build the APK on your local machine.

## 📱 Building the Android APK

### Prerequisites

Before you can build the APK, you need to install the following on your development machine:

1. **Node.js** (v18+)
   - Download: https://nodejs.org/
   - Verify: `node --version`

2. **npm** (v9+)
   - Comes with Node.js
   - Verify: `npm --version`

3. **Cordova CLI**
   ```bash
   npm install -g cordova
   ```
   - Verify: `cordova --version`

4. **Java JDK 17+**
   - Download: https://www.oracle.com/java/technologies/javase-jdk17-downloads.html
   - Verify: `java -version`

5. **Android Studio** (for Android SDK)
   - Download: https://developer.android.com/studio
   - Install Android SDK (API 34+)

6. **Android SDK Command-line Tools**
   - Install via Android Studio SDK Manager
   - Or: https://developer.android.com/studio#command-tools

7. **Environment Variables**
   ```bash
   # Add to your shell configuration (~/.bashrc, ~/.zshrc, etc.)
   export ANDROID_HOME=$HOME/Android/Sdk
   export ANDROID_SDK_ROOT=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

---

## 🚀 Build Steps

### 1. Clone the Repository

```bash
git clone https://github.com/veruca-vee/phyllotaxis.git
cd phyllotaxis/CordovaApp
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Add Android Platform (if not already added)

```bash
cordova platform add android
```

### 4. Build Debug APK

```bash
cordova build android
```

The debug APK will be created at:
```
platforms/android/app/build/outputs/apk/debug/app-debug.apk
```

### 5. Build Release APK (Recommended for Sideloading)

#### Generate a Keystore (First Time Only)

```bash
keytool -genkey -v -keystore phyllotaxis-release.keystore \
    -alias phyllotaxis \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000
```

#### Build Release APK

```bash
cordova build android --release -- --keystore=phyllotaxis-release.keystore \
    --storePassword=YOUR_PASSWORD \
    --alias=phyllotaxis \
    --password=YOUR_PASSWORD
```

The signed release APK will be created at:
```
platforms/android/app/build/outputs/apk/release/app-release.apk
```

---

## 📁 Project Structure

```
phyllotaxis/
├── CordovaApp/
│   ├── config.xml              # Cordova configuration
│   ├── package.json            # Node.js dependencies
│   ├── www/
│   │   ├── index.html          # Main HTML (mobile-optimized)
│   │   ├── phyllotaxis.js      # Phyllotaxis algorithm
│   │   ├── css/
│   │   └── img/
│   │       ├── logo.png        # App icon (replace with actual)
│   │       └── splash.png      # Splash screen (replace with actual)
│   └── platforms/
│       └── android/            # Android project files
└── ...
```

---

## 🎯 Configuration Details

### config.xml

The `config.xml` file is pre-configured with:

- **Package ID**: `com.phyllotaxis.mistral`
- **App Name**: Phyllotaxis
- **Description**: Generative art app description
- **Android Settings**:
  - Target SDK: 34
  - Min SDK: 24 (Android 7.0+)
  - Fullscreen: Enabled
  - Portrait orientation
  - Custom status bar colors
  - Splash screen configuration

### index.html

- Mobile-optimized viewport
- Touch-friendly UI
- Cordova-specific CSP (Content Security Policy)
- Safe area insets for notch support

### phyllotaxis.js

- Mobile detection
- Touch event handling
- Performance optimization (300 points on mobile)
- Adaptive scaling

---

## 📱 Sideloading the APK

### On Android Device

1. **Transfer APK to Device**
   - Use USB cable, email, or cloud storage
   - File: `app-release.apk` or `app-debug.apk`

2. **Enable Unknown Sources**
   - Go to Settings > Security > Unknown Sources
   - Enable "Allow installation from unknown sources"
   - Or on newer Android: Enable for specific app (File Manager)

3. **Install APK**
   - Open File Manager
   - Navigate to the APK file
   - Tap to install
   - Confirm installation

4. **Open App**
   - Find "Phyllotaxis" in your app drawer
   - Tap to open
   - Enjoy the generative art!

### Using ADB (Optional)

```bash
# Connect device via USB
adb devices

# Install APK
adb install platforms/android/app/build/outputs/apk/release/app-release.apk
```

---

## 🐞 Troubleshooting

### Common Issues

#### "Failed to find 'ANDROID_HOME'"
```bash
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

#### "Java not found"
```bash
# Install OpenJDK
sudo apt install openjdk-17-jdk  # Ubuntu/Debian
brew install openjdk@17          # macOS
```

#### "Gradle build failed"
```bash
# Update Gradle
cd platforms/android
./gradlew wrapper --gradle-version 8.4
```

#### "SDK not found"
```bash
# Install Android SDK via Android Studio
# Or use command line:
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

### Cordova Commands

| Command | Description |
|---------|-------------|
| `cordova platform ls` | List added platforms |
| `cordova platform remove android` | Remove Android platform |
| `cordova platform add android` | Add Android platform |
| `cordova requirements` | Check all requirements |
| `cordova clean` | Clean build files |
| `cordova build` | Build all platforms |
| `cordova build android` | Build Android only |

---

## 📝 Notes

### Replacing Placeholder Icons

The project includes placeholder icons. For production, replace:
- `www/img/logo.png` - App icon (512x512 recommended)
- `www/img/splash.png` - Splash screen (1080x1920 recommended)

### Icon Sizes

For best results, provide icons in multiple sizes:
- `res/icon/android/icon-36-ldpi.png` (36x36)
- `res/icon/android/icon-48-mdpi.png` (48x48)
- `res/icon/android/icon-72-hdpi.png` (72x72)
- `res/icon/android/icon-96-xhdpi.png` (96x96)
- `res/icon/android/icon-144-xxhdpi.png` (144x144)
- `res/icon/android/icon-192-xxxhdpi.png` (192x192)

### Splash Screen Sizes

- `res/screen/android/screen-ldpi-portrait.png` (200x320)
- `res/screen/android/screen-mdpi-portrait.png` (320x480)
- `res/screen/android/screen-hdpi-portrait.png` (480x800)
- `res/screen/android/screen-xhdpi-portrait.png` (720x1280)
- `res/screen/android/screen-xxhdpi-portrait.png` (960x1600)
- `res/screen/android/screen-xxxhdpi-portrait.png` (1080x1920)

---

## ✅ Quick Checklist

- [ ] Node.js installed
- [ ] Cordova CLI installed
- [ ] Java JDK 17+ installed
- [ ] Android Studio installed
- [ ] Android SDK installed
- [ ] Environment variables set
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Android platform added
- [ ] APK built
- [ ] APK transferred to device
- [ ] Unknown sources enabled
- [ ] APK installed

---

## 🎉 Success!

Once built, you'll have a fully functional Android APK that you can:
- Sideload on your Android device
- Share with friends
- Distribute via app stores (with proper signing)

The app will display beautiful phyllotaxis patterns with:
- Tap to change color modes
- Responsive design for all screen sizes
- Smooth performance on mobile devices

---

**Need Help?**
- Check the [Cordova Documentation](https://cordova.apache.org/docs/)
- Open an issue on [GitHub](https://github.com/veruca-vee/phyllotaxis/issues)
