# Camera Capture Feature

## Overview

The Document AI application now includes a built-in camera capture feature, allowing users to take photos of documents directly from their device's camera.

## Features

### 📷 Camera Capture Button
- Prominent button with gradient styling on the upload page
- Activates device camera (uses rear camera on mobile devices)
- Real-time video preview

### ✓ Capture Controls
- **Capture Button**: Take the photo and use it for processing
- **Cancel Button**: Close camera without capturing
- Automatic camera shutdown after capture

### 🖼️ Image Preview
- Captured photos are automatically previewed
- Shows in the same preview area as uploaded files
- Seamless integration with existing upload workflow

## How It Works

### For Desktop Users
1. Click **📷 Take Photo** button
2. Allow browser to access webcam (first time only)
3. Position document in camera view
4. Click **✓ Capture** to take photo
5. Camera closes automatically
6. Photo is ready for processing

### For Mobile Users
1. Click **📷 Take Photo** button
2. Allow app to access camera (first time only)
3. Rear camera activates automatically
4. Position document in frame
5. Click **✓ Capture** to snap photo
6. Photo is ready for analysis

## Technical Details

### Browser API
- Uses `navigator.mediaDevices.getUserMedia()` API
- Requests `environment` facing mode (rear camera on mobile)
- Fallback to user-facing camera if unavailable

### Image Format
- Captures as JPEG format
- Quality: 90% compression
- Automatic file naming: `camera-capture.jpg`

### File Integration
- Creates a proper File object from captured image
- Integrates seamlessly with existing file upload flow
- No server-side changes required

### Browser Compatibility
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support (iOS 11+)
- ✅ Mobile browsers: Full support

### Privacy & Security
- Camera access requires user permission
- No images sent to server until "Analyze Document" is clicked
- Camera stream stops immediately after capture or cancel
- No background recording or storage

## UI Elements

### Camera Button
```
📷 Take Photo
```
- Purple gradient background
- Prominent placement above file upload
- Hover effect (scales to 1.05x)

### Camera Preview
- Full-width video element (max 400px)
- Rounded corners for modern look
- Appears when camera is active

### Capture Controls
```
✓ Capture    ✗ Cancel
```
- Green capture button
- Red cancel button
- Side-by-side layout

## Use Cases

### Perfect For:
- 📱 **Mobile Document Scanning**: Quick captures on phones/tablets
- 📄 **Physical Documents**: Invoices, receipts, forms, business cards
- 🚀 **On-the-Go Processing**: Capture and analyze immediately
- 👥 **Field Work**: Sales reps, auditors, inspectors
- 📊 **Event Registration**: Capture registration forms live

### Advantages Over File Upload:
- ⚡ Faster than navigating file system
- 📸 No need to save photo first
- 🎯 Real-time framing and positioning
- 💾 No storage space used on device
- 🔄 Immediate processing workflow

## Limitations

### Camera Access Required
- User must grant camera permissions
- Some browsers may block on non-HTTPS sites (development environments)
- Corporate/school networks may restrict camera access

### Image Quality
- Depends on device camera quality
- Lighting conditions affect results
- Manual focusing may be needed for some devices

### File Types
- Only captures images (no PDF support via camera)
- For PDFs, use traditional file upload

## Troubleshooting

### "Unable to access camera" Error
**Possible Causes:**
1. Camera permissions denied
2. Camera in use by another app
3. No camera available on device
4. Browser doesn't support camera API

**Solutions:**
1. Check browser permissions for camera access
2. Close other apps using camera
3. Try a different browser
4. Use file upload instead

### Camera Preview Not Showing
1. Refresh the page
2. Check if camera is blocked by browser
3. Try HTTPS connection
4. Verify camera hardware is working

### Capture Button Not Working
1. Wait for camera to fully initialize
2. Check console for errors
3. Try clicking cancel and starting over
4. Use file upload as alternative

## Future Enhancements

Potential future improvements:
- 🔍 Zoom controls
- 💡 Flash/torch control
- 🎨 Image filters and adjustments
- 📐 Crop and rotate before processing
- 📹 Multiple page capture
- 🖼️ Gallery view of captured images

## Accessibility

- Keyboard accessible (Tab navigation)
- Screen reader compatible
- Large, clear buttons
- Visual feedback on all actions
- Alternative file upload always available

## Performance

- Minimal impact on page load
- Camera stream only active when needed
- Automatic cleanup and resource release
- Efficient image compression
- No background processing

## Security Considerations

- ✅ No images stored locally
- ✅ Camera access only when user initiates
- ✅ Automatic stream termination
- ✅ No third-party camera libraries
- ✅ Native browser APIs only
- ✅ User has full control

## Integration with Existing Features

The camera feature works seamlessly with:
- ✅ File preview system
- ✅ Authentication flow
- ✅ Document processing pipeline
- ✅ Result display
- ✅ Configuration management
- ✅ All ML models

## Browser Permissions

### First Use
When clicking "Take Photo" for the first time, browsers will show a permission prompt:

**Chrome/Edge:**
```
http://localhost:3000 wants to use your camera
[Block] [Allow]
```

**Firefox:**
```
Do you want to share your camera with localhost:3000?
[Don't Allow] [Allow]
```

**Safari:**
```
"localhost" Would Like to Access the Camera
[Don't Allow] [OK]
```

Users must click "Allow" to use the camera feature.

### Subsequent Uses
After initial permission grant:
- Camera opens immediately
- No additional prompts
- Permissions persist for the site
- Can be revoked in browser settings

## Best Practices for Users

### Document Positioning
- 📐 Keep document flat and straight
- 💡 Ensure good lighting (no shadows)
- 🎯 Center document in frame
- 📏 Fill frame with document (not too far)
- 📱 Hold device steady

### Capture Quality
- 🌟 Use natural light when possible
- 🚫 Avoid glare and reflections
- ✨ Clean camera lens before use
- 🎨 High contrast backgrounds work best
- 📸 Take multiple captures if needed

## Conclusion

The camera capture feature makes the Document AI application truly mobile-friendly and enables quick, on-the-go document processing without the need to save files first. It's intuitive, secure, and integrates seamlessly with the existing workflow.

