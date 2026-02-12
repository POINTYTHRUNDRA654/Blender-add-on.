# Desktop Tutorial Integration Add-on for Blender

A Blender add-on that integrates with a desktop tutorial application, allowing seamless communication between Blender and your tutorial software.

## Features

- **Connection Management**: Connect and disconnect from your desktop tutorial app
- **Tutorial Controls**: Navigate through tutorial steps directly from Blender
- **Step Tracking**: Mark tutorial steps as complete and track progress
- **Event System**: Send events from Blender to the tutorial application
- **Configurable Settings**: Set custom host and port for your tutorial app
- **UI Panel**: Easy-to-use sidebar panel in Blender's 3D viewport

## Installation

1. Download or clone this repository
2. Open Blender
3. Go to `Edit > Preferences > Add-ons`
4. Click `Install...` button
5. Navigate to the `__init__.py` file in this repository
6. Select it and click `Install Add-on`
7. Enable the add-on by checking the checkbox next to "Desktop Tutorial Integration"

## Configuration

1. After installing, click on the add-on name to expand preferences
2. Configure the following settings:
   - **Server Host**: The hostname/IP of your desktop tutorial app (default: localhost)
   - **Server Port**: The port number your tutorial app listens on (default: 8080)
   - **Auto Connect**: Enable to automatically connect on Blender startup

## Usage

### Accessing the Panel

1. In the 3D Viewport, press `N` to show the sidebar
2. Click on the `Tutorial` tab
3. The "Desktop Tutorial" panel will appear

### Connecting to Tutorial App

1. Make sure your desktop tutorial application is running
2. Click the `Connect to Tutorial App` button
3. The connection status will update to show "✓ Connected"

### Tutorial Controls

Once connected, you can:

- **Next Tutorial Step**: Request the next step in the tutorial sequence
- **Mark Step Complete**: Mark the current step as complete
- **Current Step Info**: View the current step number and description

### Disconnecting

- Click the `Disconnect from Tutorial App` button when you're done

## Integration with Desktop Tutorial App

This add-on expects to communicate with a desktop tutorial application via a simple protocol. The tutorial app should:

1. Listen on a configurable host and port (default: localhost:8080)
2. Accept JSON-formatted messages for events
3. Provide tutorial step information
4. Track completion status

### Example Event Format

```json
{
  "type": "action_completed",
  "data": "user_action_description",
  "timestamp": 1
}
```

## Development

### File Structure

```
Blender-add-on/
├── __init__.py          # Main add-on file
└── README.md            # This file
```

### Key Components

- **TutorialAddonPreferences**: Add-on preferences panel
- **TUTORIAL_OT_connect**: Operator to connect to tutorial app
- **TUTORIAL_OT_disconnect**: Operator to disconnect
- **TUTORIAL_OT_send_event**: Send custom events to tutorial app
- **TUTORIAL_OT_request_next_step**: Request next tutorial step
- **TUTORIAL_OT_mark_complete**: Mark current step as complete
- **TUTORIAL_PT_main_panel**: Main UI panel in 3D viewport

## Requirements

- Blender 2.80 or higher
- Python 3.x (included with Blender)
- Desktop tutorial application running on accessible host/port

## Troubleshooting

### Add-on won't enable
- Make sure you're using Blender 2.80 or higher
- Check the Blender console for error messages

### Cannot connect to tutorial app
- Verify the tutorial app is running
- Check the host and port settings in add-on preferences
- Ensure no firewall is blocking the connection

### Panel not visible
- Press `N` in the 3D Viewport to show the sidebar
- Look for the "Tutorial" tab

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues or questions, please open an issue on the GitHub repository.