# ndplot

high-dimensional viewer, by projecting onto a 3d hypercube.  Use the mouse to rotate the 3d projection hypercube.

This doesnt really work as well as I hoped it would.

The concept is:
- project onto 3d hypercube/plane
- can rotate the 3d projection freely, to view it from any angle (simply drag the mouse, with or without ctrl
key, to do this;  pressing ctrl key changes the left-right drag axis)
- can use `w` key to change the rotation axes, into a hyper-axis; and then drag the mouse, to drag around in hyperspace

This sort of works.  But I dont find being able to drag around in 4 dimensions as useful as I thought I would...

Anyway, this is what I have for now.

![](img/ndplotb.png)

I looked at the following earlier projects before writing this:

- hypertools https://github.com/ContextLab/hypertools  Seems nice.  Python, matplotlib.  Projection from hyperspace into 3 dimensions, using SVD
- https://github.com/mikasarkinjain/hyperdimensional-data-visualization  Written in 'Processing' language.  Shows 3 dimensions in the viewer, and 3 additional dimensions via red/green/blue shading.

Hypertools seems cool.  I wanted a bit more flexibility to customize how one drags around the viewport, the UI etc.  And hypertools seems to fix the projection plane to the results of SVD essentially?  Sarkin-Jain's project sounds similar to what I'm trying here.  The main reason I didnt consider using it directly is because I wanted something written in Python ideally.  I also looked briefly at how https://github.com/facebook/UETorch is implemented, or at least, what engine they are using.  They are using Unreal engine.  I think that's overkill for what I have/had in mind :-P

In other news, I think [Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home), which I'm using here, works quite well for what I want/wanted:
- handles key presses with almost no effort, and mouse drags
- opengl, of course
  - (and the opengl wrapping works pretty nicely, no major 'ow!' points or anything)
- didnt take much effort to put a 2d hud on it
