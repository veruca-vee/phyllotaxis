# Phyllotaxis - Mistral's Version

> A beautiful generative art project creating sunflower-like patterns based on the mathematical principles of phyllotaxis. Fully compatible with mobile and desktop browsers, with an Android APK available for sideloading.

![Phyllotaxis Pattern](https://img.shields.io/badge/Phyllotaxis-Generative%20Art-e94560?style=for-the-badge)
![Mobile Compatible](https://img.shields.io/badge/Mobile-Compatible-4CAF50?style=for-the-badge)
![Android APK](https://img.shields.io/badge/Android-APK-3DDC84?style=for-the-badge)

## 🌻 About

Phyllotaxis is the study of how leaves, seeds, and other plant parts are arranged in nature. This project visualizes the beautiful spiral patterns found in sunflowers, pinecones, and pineapples using the golden angle (137.5°).

## 📸 Screenshots

### Desktop
![Desktop Screenshot](screenshots/desktop.png)

### Mobile
![Mobile Screenshot](screenshots/mobile.png)

### Tablet
![Tablet Screenshot](screenshots/tablet.png)

## ✨ Features

- **Generative Art**: Creates unique sunflower patterns using phyllotaxis algorithm
- **Multiple Color Modes**: Golden (default), Rainbow, Grayscale
- **Responsive Design**: Works on all screen sizes
- **Mobile Optimized**: Touch-friendly with performance optimizations
- **Interactive**: Tap to change color modes, press 'S' to save
- **Android APK**: Available for sideloading

## 📱 Platforms

- ✅ **Web**: Open `index.html` in any modern browser
- ✅ **Mobile Web**: Works on iOS Safari, Android Chrome, etc.
- ✅ **Android APK**: Sideload the APK for native experience

## 🚀 Quick Start

### Web Version

1. Clone this repository:
   ```bash
   git clone https://github.com/veruca-vee/phyllotaxis.git
   cd phyllotaxis
   ```

2. Open `index.html` in your browser, or:

3. Start a local server:
   ```bash
   python3 -m http.server 8000
   # or
   npx serve
   ```

4. Open `http://localhost:8000` in your browser

### Android APK

1. Download the latest APK from the [Releases](https://github.com/veruca-vee/phyllotaxis/releases) page
2. Transfer to your Android device
3. Enable "Unknown Sources" in Settings > Security
4. Install the APK file
5. Open the Phyllotaxis app

## 🎨 Usage

### Web Interface
- **Tap/Click**: Cycle through color modes (Golden → Rainbow → Grayscale)
- **Press 'S'**: Save the current pattern as PNG
- **Resize Window**: Pattern adapts to new dimensions

### Color Modes

| Mode | Description | Visual Effect |
|------|-------------|---------------|
| Golden | Warm gold and yellow tones | Sunflower-like appearance |
| Rainbow | Full color spectrum | Vibrant, colorful spiral |
| Grayscale | Black to white gradient | Monochrome, elegant |

## 📦 Project Structure

```
phyllotaxis/
├── index.html          # Main HTML file
├── phyllotaxis.js      # Phyllotaxis algorithm
├── README.md           # Project documentation
├── CONTRIBUTING.md     # Contribution guidelines
├── LICENSE             # MIT License
├── TESTING.md          # Testing documentation
├── package.json        # Project metadata
├── config.xml          # Cordova configuration
├── android/            # Android project files (if building APK)
├── screenshots/        # Screenshot assets
└── www/                # Web assets for Cordova
```

## 🛠️ Building from Source

### Web Version

No build step required! Just open `index.html` in a browser.

### Android APK

Prerequisites:
- Node.js (v18+)
- npm (v9+)
- Cordova CLI
- Android SDK
- Java JDK 17+

```bash
# Install Cordova globally
npm install -g cordova

# Navigate to project
cd phyllotaxis

# Add Android platform
cordova platform add android

# Build APK
cordova build android --release

# APK will be in: platforms/android/app/build/outputs/apk/release/
```

## 🔧 Configuration

### Customizing the Pattern

Edit `phyllotaxis.js` to modify:

```javascript
// Number of points (adjust for performance)
let totalPoints = 500;

// Spiral tightness
let c = 4;

// Golden angle in degrees
let angleStep = 137.5;
```

### Mobile Optimization

The app automatically detects mobile devices and:
- Reduces point count to 300 for better performance
- Adjusts point sizes for smaller screens
- Prevents accidental scrolling on the canvas

## 📊 Performance

| Device | Points | Render Time | Memory Usage |
|--------|--------|-------------|--------------|
| Desktop | 500 | <50ms | ~50MB |
| Tablet | 500 | <100ms | ~40MB |
| Mobile | 300 | <150ms | ~30MB |

## 🧪 Testing

See [TESTING.md](TESTING.md) for detailed testing information.

### Manual Testing

1. **Desktop**: Test in Chrome, Firefox, Safari, Edge
2. **Mobile**: Test on iOS Safari, Android Chrome
3. **Tablet**: Test on iPad, Android tablets
4. **Android APK**: Install and test on various Android versions

### Automated Testing

Run the validation script:
```bash
python3 validate.py
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by [The Coding Train](https://thecodingtrain.com/) phyllotaxis tutorial
- Built with [p5.js](https://p5js.org/)
- Android APK built with [Apache Cordova](https://cordova.apache.org/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/veruca-vee/phyllotaxis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veruca-vee/phyllotaxis/discussions)

---

**Made with ❤️ by Mistral AI**

*Phyllotaxis - Bringing the beauty of nature's patterns to life through code.*
