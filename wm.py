from Xlib.display import Display
from Xlib import X, XK
import subprocess
import config

display = Display()
root = display.screen().root
root.change_attributes(event_mask=X.SubstructureRedirectMask)

root.grab_key(display.keysym_to_keycode(XK.string_to_keysym("F1")), X.Mod1Mask, 1,
        X.GrabModeAsync, X.GrabModeAsync)
root.grab_button(1, X.Mod1Mask, 1, X.ButtonPressMask|X.ButtonReleaseMask|X.PointerMotionMask,
        X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE)
root.grab_button(3, X.Mod1Mask, 1, X.ButtonPressMask|X.ButtonReleaseMask|X.PointerMotionMask,
        X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE)
root.grab_key(display.keysym_to_keycode(XK.string_to_keysym("t")), X.Mod1Mask, 1,
        X.GrabModeAsync, X.GrabModeAsync)

start = None
while 1:
    event = display.next_event()
    if event.type == X.MapRequest:
        event.window.map()
    elif event.type == X.ConfigureRequest:
        window = event.window
        window.configure(
            x=event.x,
            y=event.y,
            width=event.width,
            height=event.height,
            border_width=event.border_width,
            stack_mode=event.stack_mode
        )
    if event.type == X.KeyPress:
        keysym = display.keycode_to_keysym(event.detail, 0)

        if keysym == XK.string_to_keysym("t"):
            subprocess.Popen(config.term)

        elif keysym == XK.string_to_keysym("F1") and event.child != X.NONE:
            event.child.configure(stack_mode=X.Above)

    elif event.type == X.ButtonPress and event.child != X.NONE:
        attr = event.child.get_geometry()
        start = event
    elif event.type == X.MotionNotify and start:
        xdiff = event.root_x - start.root_x
        ydiff = event.root_y - start.root_y
        start.child.configure(
            x = attr.x + (start.detail == 1 and xdiff or 0),
            y = attr.y + (start.detail == 1 and ydiff or 0),
            width = max(1, attr.width + (start.detail == 3 and xdiff or 0)),
            height = max(1, attr.height + (start.detail == 3 and ydiff or 0)))
    elif event.type == X.ButtonRelease:
        start = None