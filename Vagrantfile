Vagrant::Config.run do |config|
    config.vm.box     = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.forward_port 27017, 27018
    config.vm.provision "shell", path: "provision.sh"
end
