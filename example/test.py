import bimpy

ctx = bimpy.Context()
    
ctx.init(1200, 1200, "Hello")   
    
with ctx:   
    bimpy.themes.set_light_theme()
    
opened = bimpy.Bool(True)    
    
a = 0.0 
    
mylist = ["aaa", "bbb", "ccc"]  
    
selectedItem = bimpy.Int()   
    
vals = [0., 0.1, 0.2 ,0.1, 0.4, 0.2]    
    
while(not ctx.should_close()):  
    ctx.new_frame() 
        
    bimpy.show_test_window() 
        
    if opened.value:    
        if bimpy.begin("Hello!", flags = bimpy.WindowFlags.ShowBorders, opened = opened): 
            bimpy.columns(4, "mycolumns")    
            bimpy.separator()    
            bimpy.text("Some text")  
            bimpy.next_column()  
            bimpy.text("Some text")  
            bimpy.next_column()  
            bimpy.text("Some text")  
            bimpy.next_column()  
            bimpy.text("Some text")  
            bimpy.separator()    
            bimpy.columns(1) 
                
            if bimpy.button("Some button"):  
                a = 0   
                print("!!!")    
                    
            bimpy.progress_bar(a)    
                
            bimpy.combo("Combo!", selectedItem, mylist)  
                
            bimpy.push_item_width(-10.0) 
            bimpy.plot_lines("Some plot", vals, graph_size = bimpy.Vec2(0, 300))  
            bimpy.pop_item_width()   
            
            a += 0.01
        bimpy.end()
    
    ctx.render()
