# GalDir
Simple no-fuss Directory-tree based Web Gallery

Just point the app at your folder full of images and you'll get a photo gallery!

## Installation
### Direct install
Requirements:
- Python 3 (Tested with 3.7.3 and 3.6.8)
- Whatever Pillow requires for your platform

Installation Steps:

1. Edit config.ini to your requirements.  The entries beginning with 'galdir.' are likely the only things you care about.
1. Clone this git repo
   ```
   git clone https://github.com/samburney/galdir.git
   ```
1. Install Python dependencies
   ```
   pip install -e galdir/
   ```
1. Run the server
   ```
   pserve config.ini
   ```
By default this should now give you a Web Gallery at http://\<server\>:6543/ based on the contents of the albums directory configured in config.ini.

### Docker
#### Minimum docker CLI
```
docker run -p 0.0.0.0:6543:6543 samburney/galdir:latest
```

#### Docker Compose
Example docker-composer.yml
```
version: '2.4'

services:
  galdir:
    image: 'samburney/galdir:latest'
    restart: 'unless-stopped'
    environment:
      GALDIR_SITENAME: 'Gallery Site Name'
      GALDIR_IMAGES_PERPAGE: '12'
    volumes:
      - '/etc/localtime:/etc/localtime:ro'
      - './data/cache:/usr/local/share/galdir/galdir/cache'
      - './data/albums:/usr/local/share/galdir/albums'
    ports:
      - '6543:6543/tcp'
```

#### Available Environment Variables
- GALDIR_LISTEN: Listen address/port for the web server inside of the Docker container.  Defaults to 0.0.0.0:6543.
- GALDIR_SITENAME: Name of this site - is used in titles and the Navbar.  Defaults to GalDir.
- GALDIR_ALBUMS: Defaults to 'albums', which maps to ```/usr/local/share/galdir/albums/```
- GALDIR_CACHE: Defaults to 'cache', which maps to ```/usr/local/share/galdir/galdir/cache/``` within the Docker container.
- GALDIR_IMAGES_PERPAGE: Number of images displayed per page.  Defaults to 12.

## License
This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/.
