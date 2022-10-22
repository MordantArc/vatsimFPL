# vatsimFPL
Takes latest filed Vatsim flightplan and display.

# Main Function:
So you filed your flightplan, you're in the cockpit. You call up clearance and oh no!

They alter your flightplan!
Whatever will you do?!

Well with this program, you will be saved the agony of asking again and again to repeat your routes(they can get so complicated!). It is essentially a virtual kneeboard with all the info of your flightplan, updating every 20s including ATC adjusted routes. They change your route? It'll change with it.

# How to set up:
As of right now, all you need to do is find your Vatsim CID and enter it into the 'vatsimcid.txt' file. It will then read this and be able to access the public API data from Vatism. The only lib I am using outside of integrated python functions is the [Carnegie-Mellon CS Academy](https://academy.cs.cmu.edu/desktop) lib so it can display a mini gui. I plan to use a more purpose-built gui, but this is one that I already had experience with and was incredibly simple to use. It should be in the git already, but you may need to add it to your lib using "pip install cmu-graphics".

# Final Notes:
Please improve on this! 

I am making this to help the community, and any improvements to the program that help the community are encouraged!

This is also my first program, so please give me feedback so I can improve my work. 
Thanks for visiting :)
