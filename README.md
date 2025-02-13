# ZeroKun265's Arch Linux
My arch setup scripts and configs, hopefully up to date

# 1. Installation
No script is made for the installation as there is a possibility of different partitions or dual boots, i can't be bothered to make scripts taking those into account, a regular arch install can be followed

## Basic steps to get a first install with no secure boot and minimal packages:

- `loadkeys <keymap>`
    - the italian keymap is called *it*
- `iwcl`
    - `device list`
    - `station <name> scan`
    - `station <name> get-networks`
    - `station <name> connect <SSID>`
- `ping google.com`
- `imedatectl`
- `fdisk -l`
- `fdisk`
    - Follow fdisk instructions to format drives as needed, setup an EFI partition and a root partition (optionals: home partition and swap partitions)
- `mkfs.ext4 /dev/root_part` (same for */dev/home:part*)
- `mkfs.fat /dev/EFI_part`
- `mkswap /dev/swap_part`
- `mount /dev/root_part /mnt`
    - `mount --mkdir /dev/home_part /mnt/home` if a home partition was made
- `mount --mkdir /dev/EFI_part /mnt/boot`
- `swapon /dev/swap_part` if a swap partition was made
- `pacstrap -K /mnt base linux linux-firmware nano iwd <cpu-brand>-ucode vim vi zsh`
- `genfstab -U /mnt >> /mnt/etc/fstab`
- `arch-chroot /mnt`
- `ls -sf /usr/share/<Region>/<City> /etc/localtime`
- `hwclock -systohc`
- Uncomment necessary locales in */etc/locale.gen* and then run the commands
- `locale-gen`
- Then create a file */etc/locale.conf* and type `LANG=<locale>`
    - for example: `LANG=en_US.UTF-8`
- Then create a file */etc/vconsole.conf* and type `KEYMAP<keymap>`
    - The one in step 1
- `echo <your-host-name> > /etc/hostname`
- `mkinitcpio -P`
- `passwd`
- `sudo pacman -S grub efibootmgr`
- `grubinstall --target=x86_64-efi --efi-directory=/mnt/boot --bootloader-id=<whatever-id>`
- `nano /etc/defautl/grub` and uncomment the line to enable os prober
- `grub-mkconfig -o /boot/grub/grub.cfg`

## Create a user (don't use root!)

- `useradd -m -G <groups> -s <path to default shell> <username>`
    - recommended to add the user to the group *wheel*, for sudo usage
- As root, run: `visudo`, scroll down to the %wheel line and enable sudo for the wheel group

## Install yay
- `sudo pacman -S --needed git base-devel`
- `git clone https://aur.archlinux.org/yay.git`
- `cd yay`
- `makepkg -si`

## 2. Bare minimum KDE:
We can install kde, sddm, network manager and other stuff for a basic setup using the `bare_minimum_kde.sh` script

## 3. Installing all the other packages
Now that we have a gui, we can install all the other packages
Just run `yay -S - < packages.txt`

## 4. Dotfiles and other configs
You can run the `copy-config.sh` script (with sudo or root) to automatically clone all the config files and dot files into the correct places (hopefully i kept them all up to date)

## 5. Kde theming
The theme coulb be anyone, the latest one i use is kde catpuccin, and sddm catpuccin, for the instructions to install them check their github pages since they could change 

## 6. Local scripts and apps
I prefer having my scripts and downloaded random icons etc.. in a `.local_bin` folder instead of the regular `.local` folder for simplicity
Run the `local_bin.sh` script to copy that into the home folder

##  7. Dual boot
If you're dual booting, chances are you lost access to windows, the *packages.txt* contains os-prober, so you can:
- `nano /etc/defautl/grub` and uncomment the line to enable os prober if not already enabled
- `grub--mkconfig -o /boot/grub.cfg`

