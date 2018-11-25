import bimpy
import pkg_resources
print(pkg_resources.get_distribution("bimpy").version)

ctx = bimpy.Context()

ctx.init(600, 600, "Sliders")

with ctx:
    bimpy.themes.set_light_theme()

#slider float3    
f1 = bimpy.Float();
f2 = bimpy.Float();
f3 = bimpy.Float();

#vertical slider 
f4 = bimpy.Float();
f5 = bimpy.Float();
    
#slider_angle
f6 = bimpy.Float();

#slider int2
i1 = bimpy.Int();
i2 = bimpy.Int();

while(not ctx.should_close()):
    ctx.new_frame()

    bimpy.begin("Sliders!", flags=bimpy.WindowFlags.AlwaysAutoResize)
    
    bimpy.slider_float3("float3", f1, f2, f3, 0.0, 1.0)
    
    bimpy.v_slider_float("v_slider", bimpy.Vec2(20, 300), f4, 0.0, 1.0)
    
    bimpy.same_line()
    
    bimpy.v_slider_float("v_slider2", bimpy.Vec2(50, 300), f5, -100.0, 100.0, "[%.1f]")
    
    bimpy.slider_angle("slider_angle", f6, -100.0, 100.0)
    
    bimpy.slider_int2("slider_int2", i1, i2, 0, 100)
    
    bimpy.end()

    ctx.render()
