I wanted a PGP key for signing my commits and email, held on hardware so it could not be copied off my laptop. I have two YubiKeys: a small one that lives in the laptop and one on my keychain. I wanted the same key on both, and no copy anywhere else. This is how that went, including the parts that did not work the first time.

## The constraint nobody mentions up front

A key generated inside a YubiKey can never leave it. That is the point of the device, and it means two YubiKeys cannot share a key that either of them created. If you want one key on two devices, the key has to be made somewhere else and loaded onto each.

So for a few minutes the private key has to exist outside the hardware. The question is where.

## Making the key in memory

My laptop's disk is not encrypted yet. A private key written to it, even briefly, could linger in flash storage after deletion. A passphrase would protect it, but then I would be managing a passphrase for a file I intended to destroy.

The answer was to never write it to disk. Linux keeps a per-user directory in memory (`$XDG_RUNTIME_DIR`, a tmpfs). I pointed GnuPG at a keyring there, generated the key with no passphrase, loaded it onto both YubiKeys, and deleted the directory. A reboot would have wiped it too.

One caveat: hibernation writes memory to disk. I did the whole thing in one sitting with the lid open.

## The shape of the key

The usual advice is a master key kept offline and subkeys on the card. I did not want an offline anything. I made the primary key do both certification and signing, with one encryption subkey:

`gpg --quick-generate-key "Name <email>" ed25519 cert,sign never`

`gpg --quick-add-key FINGERPRINT cv25519 encr never`

The whole key fits on a card that way. Nothing is left over that needs a safe.

## Loading two cards

Moving a key to a card (`keytocard` in `gpg --edit-key`) removes it from the keyring. For the second card you have to import it again from an export, which is why I kept one in the same memory directory until both cards were done.

Things that cost me time:

- **GnuPG could not see the card.** I had the system smart-card service (`pcscd`) running, and GnuPG's own card driver fought it. One line, `disable-ccid` in `scdaemon.conf`, fixed it.
- **Three different PINs.** The YubiKey's login side has a PIN. The PGP side has its own PIN and a separate Admin PIN, with factory defaults of `123456` and `12345678`. Typing the wrong one into the wrong prompt uses up tries.
- **`ykman` kills GnuPG's card process** to get the card to itself, which locks the card again. I stopped using it for routine checks.

## Touch to sign

By default, once the PIN is entered, any program on the machine can sign as me for as long as the key is plugged in. I turned on the touch requirement for signatures, so each one needs a tap, with one tap covering 15 seconds.

GnuPG shows nothing on screen when it is waiting for a tap. The key blinks, and after about 15 seconds the signature fails with "Timeout". A small program called `yubikey-touch-detector` puts up a notification instead, which made this usable.

Scheduled jobs that commit on their own cannot tap a key. Those opt out of signing explicitly.

## Publishing it

A public key nobody can find is not much use. Mine is in four places: a file on this site, a Web Key Directory on this domain so mail programs can find it from my address, my GitHub account, and keys.openpgp.org. The fingerprint is on my homepage and in my email footer. The value of repeating it is that a forged key would have to match in all of those places.

## What I gave up

There is no backup. If I lose one YubiKey I keep working on the other, but I cannot clone it onto a replacement, so that would mean a new key. If I lose both, anything encrypted to this key is gone. I kept one file, a revocation certificate, so I can declare the key dead if that happens.

For signing, that trade is easy: a signing key is replaceable. For encrypted mail it is a real cost, and I would think harder before relying on it for anything I need to read in five years.
