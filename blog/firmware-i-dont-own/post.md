I spent a weekend trying to make my laptop sleep properly. By the end I had patched one firmware, worked around four others, and run into a wall I'm not allowed to climb. The wall is the interesting part.

The laptop is a System76 Lemur Pro running Linux. I bought it partly because System76 publishes a lot of its firmware as open source. That turned out to matter more than I expected, in both directions.

## The part I could fix

It started small. When the laptop sleeps, the power light blinks once a second. In a dark room it's a strobe light. There's no setting for it, because the blink isn't controlled by the operating system at all. It's hard-coded in the embedded controller, the little chip that runs the keyboard, the fan and the power button.

On most laptops that's the end of the story. On this one, the embedded controller's source code is public. So I read it, found the four lines that toggle the light, and replaced them with one line that turns it off. Then, before flashing anything, I rebuilt System76's unmodified source with the same compiler version they use and got a file **byte-for-byte identical** to their official firmware. That proved my build process matched theirs, so the only difference in my version was the change I made. I flashed it. The light is dark now.

That's what owning a device is supposed to feel like: you can see how it works, and when it does something you don't want, you can change it.

## The parts I could only work around

The real goal was bigger: make sleep reliable when the laptop is docked to my monitors. It wasn't. Roughly one wake in twelve, something didn't come back. Sometimes the Thunderbolt connection to the dock, sometimes the Wi-Fi card, sometimes both, and occasionally the next sleep would hang the whole machine.

Each of those has a fix of sorts, but the fixes are all the same shape: since the device can't be trusted to wake up properly, reset it around every sleep. Unplug the Wi-Fi card from the bus in software before sleeping, and plug it back in on wake. Disconnect the Thunderbolt driver before sleep, and reconnect it fresh afterwards. It works. It's also a hack layered on top of firmware I can't read.

The monitor was worse. My second screen is daisy-chained through the first. After the laptop sleeps, the first monitor often stops passing a signal to the second. The laptop was sending a picture, the connection was up, and the screen still said "no signal". The only thing that fixed it was pressing the monitor's power button. The manufacturer has a firmware update whose release notes describe exactly this bug, and I was already running it.

## The wall

Then I tried to get the laptop into the kind of sleep phones and Macs use: the system stays technically on but powers almost everything down, so it can wake instantly from a keypress or from plugging in a cable. On this laptop that sleep mode drained about 4 watts, roughly ten times what it should.

Finding out why meant reading the chip's own power counters. Three things were keeping it awake.

**The display never powered down,** because a flag in the laptop's video BIOS turns off a power-saving feature (panel self-refresh) the screen supports. Linux lets me override that flag, so I did.

**The firmware never tells the operating system the laptop supports this sleep mode.** The BIOS sets that capability bit to zero. Linux tries anyway, and gets partway.

**The GPU's video engine never went idle** after a regular sleep, until the next reboot. Nothing on my system was using it. As far as I can tell from the logs, the GPU's security firmware expects to talk to Intel's Management Engine, a separate closed processor inside the chipset. System76 disables the Management Engine for privacy reasons. After a regular sleep, the GPU firmware can't finish restarting without it, and the video engine stays awake waiting.

With those addressed, the chip went from its shallowest idle state to its second-deepest, and the drain roughly halved. It still doesn't reach the deepest state.

And here is where I stop. The GPU firmware that decides when the video engine sleeps is closed and **cryptographically signed by Intel**. The chip checks that signature against a key burned into the silicon and refuses to run anything else. I can read counters that show what the firmware decided. I can't read the firmware, and I can't change it. Nobody outside Intel can.

## Whose job is this?

The honest answer to "who's responsible for fixing this" is: nobody in particular, and certainly nobody legally.

I bought the hardware. The software and firmware on it I only license, under terms that disclaim almost everything. Getting around the locks on my own device can itself be illegal in the US: Section 1201 of the copyright law bans circumventing technical protection measures unless the Copyright Office grants an exemption, and those are only reviewed every three years. Nothing requires a manufacturer to keep fixing security or reliability bugs in a device for any particular length of time. And because courts mostly act after a concrete injury, there's no practical way to challenge a design that predictably wastes power or opens attack surface until someone is actually harmed.

Some of this is changing. The EU's Cyber Resilience Act is starting to make hardware makers responsible for handling vulnerabilities in their firmware, with fuller obligations from 2027. Right-to-repair laws are passing state by state in the US. But neither requires that the owner be able to inspect or fix the firmware in their own machine.

I don't think Intel or System76 are villains here. System76 made a defensible privacy choice by disabling the Management Engine, and they open-sourced the firmware that let me fix the light. Intel signs its firmware partly for real security reasons: firmware runs with deep access, and unsigned firmware would be a gift to malware. But the result is a machine where the parts I can fix, I can fix because someone chose to let me, and the parts I can't fix, I can't fix because someone chose otherwise. The person who paid for the device had no say in either choice.

## What would actually help

None of these require giving up security:

- **Let owners see what the firmware is deciding,** and why. A documented interface for "why isn't this part of the chip sleeping" would have saved me a weekend.
- **Let owners turn off what they don't need.** If a signed component misbehaves in a way that only affects the owner's own machine, the owner should be able to disable it.
- **Require vendors to support the sleep and power modes they ship.** Advertising a capability in the hardware and disabling it in the firmware, without saying so, shouldn't be invisible to buyers.
- **Make the Section 1201 exemption process work for owners fixing their own hardware,** not just for the narrow categories it covers today.

The embedded controller showed what the alternative looks like. When the source is open, a bug is a weekend project for anyone who cares enough. When it's closed and signed, a bug is a support ticket and a wait.

I'm sending what I found to System76 and Intel, with the logs. If you've hit the same wall on your own hardware, I'd like to hear about it.
