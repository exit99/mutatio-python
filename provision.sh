# Downloads MongoDB Version 1.2.2 to the Home Dir
# Extracts it and moves the contents into the /var/mongodb folder
# Creates a symlink from /var/mongodb/mongod to /usr/local/sbin
cd ~/
wget http://downloads.mongodb.org/linux/mongodb-linux-x86_64-1.2.2.tgz
tar -xf mongodb-linux-x86_64-1.2.2.tgz
mkdir -p /var/mongodb
mv mongodb-linux-x86_64-1.2.2/* /var/mongodb/
ln -nfs /var/mongodb/bin/mongod /usr/local/sbin
 
# Ensures the required folders exist for MongoDB to run properly
mkdir -p /data/db
mkdir -p /usr/local/mongodb/logs
 
# Downloads the MongoDB init script to the /etc/init.d/ folder
# Renames it to mongodb and makes it executable
cd /etc/init.d/
wget http://gist.github.com/raw/162954/f5d6434099b192f2da979a0356f4ec931189ad07/gistfile1.sh
mv gistfile1.sh mongodb
chmod +x mongodb
 
# Ensure MongoDB starts up automatically after every system (re)boot
update-rc.d mongodb start 51 S .
 
# Starts up MongoDB right now
/etc/init.d/mongodb start
