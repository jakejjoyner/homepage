I wanted a PGP key for signing my commits and email, held on hardware so it could not be copied off my laptop. I have two YubiKeys: one that stays in the laptop and one on my keychain. I wanted the same key on both. I got there twice in two days, because my first design was wrong.

## The constraint nobody mentions up front

A key generated inside a YubiKey can never leave it. That is the point of the device, and it means two YubiKeys cannot share a key that either of them created. If you want one key on two devices, the key has to be made somewhere else and loaded onto each.

So for a few minutes the private key has to exist outside the hardware. The question is where.

## Making the key in memory

My laptop's disk is not encrypted yet. A private key written to it, even briefly, could linger in flash storage after deletion.

The answer was to never write it to disk. Linux keeps a per-user directory in memory (`$XDG_RUNTIME_DIR`, a tmpfs). I pointed GnuPG at a keyring there, generated the key, loaded it onto both YubiKeys, and deleted the directory. A reboot would have wiped it too. Hibernation writes memory to disk, so I did it in one sitting with the lid open.

## First attempt: no backup

The usual advice is a master key kept offline, with subkeys on the cards. I did not want an offline anything, so the first time I put the whole key on both cards and kept no copy. Two YubiKeys felt like a backup.

A day later I wrote down what that cost: if I lost one key I could not clone the other onto a replacement, and if I lost both, anything encrypted to the key was gone for good. Reading my own sentence, I decided I did not accept that. The key could not be extracted from the cards to back it up, so the only fix was a new key. I revoked the first one. It had been public for one day.

## Second attempt: the usual advice

The second key follows the standard layout:

`gpg --quick-generate-key "Name <email>" ed25519 cert never`

`gpg --quick-add-key FINGERPRINT ed25519 sign never`

`gpg --quick-add-key FINGERPRINT cv25519 encr never`

The first line makes a master key that can only certify. The other two add a signing subkey and an encryption subkey. The subkeys go on both YubiKeys. The master key goes on paper and nowhere else.

## The paper

A tool called `paperkey` strips a secret key down to the part that is actually secret and prints it as rows of hex with a checksum on each row. For this key that is about twenty short rows. Restoring is the reverse: type the rows into a file and combine them with the public key.

`paperkey --pubring public.gpg --secrets typed-page.txt | gpg --import`

Two things I would not skip:

- **Test the restore before trusting the page.** I rebuilt the key from the page text and compared it byte for byte with the original, while the original still existed.
- **Give the key a passphrase, and keep it somewhere else.** The page is locked by it. The page and the passphrase are each useless alone, so they must never be stored together.

## Loading two cards

Moving a key to a card (`keytocard` in `gpg --edit-key`) removes it from the keyring, so the second card needs the key imported again from an export kept in the same memory directory.

Things that cost me time:

- **GnuPG could not see the card.** The system smart-card service (`pcscd`) was running and GnuPG's own card driver fought it. One line, `disable-ccid` in `scdaemon.conf`, fixed it.
- **Three different PINs.** The YubiKey's login side has a PIN. The PGP side has its own PIN and a separate Admin PIN, with factory defaults of `123456` and `12345678`. The Admin PIN allows three wrong tries.
- **`ykman` kills GnuPG's card process** to get the card to itself, which locks the card again.
- **Reloading a key resets its touch setting.** I had to turn touch-to-sign back on after the second key went on.

## Touch to sign

By default, once the PIN is entered, any program on the machine can sign as me for as long as the key is plugged in. I turned on the touch requirement, so each signature needs a tap, with one tap covering 15 seconds.

GnuPG shows nothing on screen when it is waiting for a tap. The key blinks, and after about 15 seconds the signature fails with "Timeout". A small program called `yubikey-touch-detector` puts up a notification instead.

## The mistake I did not expect

I printed the backup page and its passphrase. Afterwards I checked where the print system keeps its work, and found it had saved the full contents of every page I printed that day, in plain text, on the unencrypted disk. CUPS keeps job files for a day by default.

I overwrote and deleted them and set `PreserveJobFiles No`. The lesson is the general one: the secret is only as contained as every program it passes through, and the printer queue is a program.

## Publishing it

A public key nobody can find is not much use. Mine is in four places: a file on this site, a Web Key Directory on this domain so mail programs can find it from my address, my GitHub account, and keys.openpgp.org. The fingerprint is on my homepage and in my email footer. A forged key would have to match in all of them.

## What I would tell myself two days ago

Do the standard thing first. The offline master key looked like ceremony until I wrote out what its absence cost. And decide what you would do if you lost everything before you make the key, not after you have published it.
