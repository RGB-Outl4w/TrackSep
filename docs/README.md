# TrackSep

**TrackSep** is a PyQt5-based application designed to separate video and audio tracks from multimedia files using FFmpeg. It features a user-friendly graphical interface for easy configuration and processing.

## Features
- Extract video and audio streams from multimedia files.
- Customizable output formats, codecs, and bitrates.
- Built-in logging system to track progress and debug errors.
- Flexible settings with options for themes and dark mode.

## Requirements
- Python 3.7 or higher
- FFmpeg installed and accessible from the system PATH
- PyQt5 library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/RGB-Outl4w/TrackSep.git
   cd TrackSep
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python -m src.main
   ```

## Usage
1. Launch the application.
2. Select the input file using the "Browse" button.
3. Choose the desired video and audio streams from the dropdown menus.
4. Specify the output folder and file templates (optional).
5. Click "Extract" to process the file.
6. View progress and logs directly within the app.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed information about your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Built with PyQt5 for the GUI.
- Powered by FFmpeg for multimedia processing.

## Contact
For questions, suggestions, or bug reports, open an issue on the GitHub repository.
