yay -S networkmanager plasma-meta kde-applications-meta sof-firmware sddm libpipewire pipewire pipewire-alsa pipewire-audio pipewire-jack pipewire-pulse wireplumber bluez bluedevil reflector

systemctl enable sddm --now
systemctl enable networkmanager --now
systemctl enable bluetooth.service --now
sudo reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
