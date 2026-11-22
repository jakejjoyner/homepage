My laptop ran hot for months. The fan would sit silent, spin up hard, stop, and do it again, even when the machine was doing almost nothing. The cause turned out to be one number in the firmware, left over from a processor released in 2018.

## The symptom

The laptop is a System76 Lemur Pro (lemp13-b) with an Intel Core Ultra 5 125U. At 5 to 9 percent CPU load the fan cycled between off and about 5,400 RPM. Linux keeps a counter of how many times the processor has slowed itself down to avoid overheating. After 24 days of uptime mine read about 13 million.

System76 support looked at my numbers, agreed it was running hotter than it should, and offered a repair. Before shipping the laptop anywhere I wanted to know whether the hardware was actually at fault.

## Ruling out the hardware

I took the bottom cover off. No dust, the heat pipe was intact and got hot along its whole length under load, and the heatsink sat level. Then I measured how well it cooled: at 5 watts the processor sat at 62 °C, and at 15 watts with every core busy it reached 79 °C. That is a cooler doing its job. Whatever was wrong, it was not the thermal paste.

## Two thermometers that disagreed

The laptop has two views of the processor's temperature. The operating system reads it directly from the chip. The embedded controller, the small separate chip that runs the fan, reads it over its own wire and decides the fan speed from that.

I compared them side by side. The embedded controller was consistently about 10 °C low: 74 °C when the processor reported 84, 53 when it reported 64.

## One constant

System76 publishes the embedded controller's source code, so I could read how it gets its number. The processor does not report an absolute temperature on that wire. It reports how far it is below its maximum. To turn that into degrees you add the maximum, and the code has the maximum written in as a constant:

`// Tjunction = 100C for i7-8565U (and probably the same for all WHL-U)`

`#define T_JUNCTION ((int16_t)100)`

The i7-8565U is a 2018 processor with a 100 °C limit. Mine has a 110 °C limit. Intel's specification says so, and so does the chip when Linux asks it. Every temperature the fan controller computed was therefore 10 °C too low.

The fan table for this model keeps the fan off below 70 °C and steps up from there. With the offset, "70" really meant 80. The fan stayed off until the processor was already hot, then came on hard, cooled it past the threshold, and switched off again. That was the cycling. The processor spent its days near the limit, which was the throttling.

## The workaround

The embedded controller can be told to stop deciding the fan speed and take orders. I put it in that mode and run a small program that reads the correct temperature from the operating system and sets the fan from a smooth curve: on at 60 °C, full speed at 92 °C.

Since then the fan runs steadily and quietly, the processor stays between 56 and 67 °C in ordinary use, and the throttle counter read 18 an hour after boot instead of climbing by about half a million a day.

## Upstream

I sent the analysis to System76 support. A few days later another Lemur Pro owner, with a different processor, reported the same thing on the firmware's issue tracker ([issue 578](https://github.com/system76/ec/issues/578)), and I added my measurements there. The firmware's maintainer has since opened a rewrite of the temperature code that asks the processor for its real maximum instead of assuming one ([pull request 580](https://github.com/system76/ec/pull/580)). It is still in progress as I write this.

## What I take from it

The bug was a comment that said "probably the same", carried forward to processors nobody checked it against. Nothing caught it, because a wrong constant does not crash anything. It makes a fan come on late.

I could find it only because the source was published. On most laptops the same number is inside a binary nobody outside the manufacturer can read, and the owner's choices are to send the machine in for a repair it does not need, or live with it.
