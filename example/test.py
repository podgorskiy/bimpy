import impy

ctx = impy.Context()
    
ctx.init(1200, 1200, "Hello")   
    
with ctx:   
    impy.themes.set_light_theme()
    
opened = impy.Bool(True)    
    
a = 0.0 
    
mylist = ["aaa", "bbb", "ccc"]  
    
selectedItem = impy.Int()   
    
vals = [0., 0.1, 0.2 ,0.1, 0.4, 0.2]    
    
while(not ctx.should_close()):  
    ctx.new_frame() 
        
    impy.show_test_window() 
        
    if opened.value:    
        if impy.begin("Hello!", flags = impy.WindowFlags.ShowBorders, opened = opened): 
            impy.columns(4, "mycolumns")    
            impy.separator()    
            impy.text("Some text")  
            impy.next_column()  
            impy.text("Some text")  
            impy.next_column()  
            impy.text("Some text")  
            impy.next_column()  
            impy.text("Some text")  
            impy.separator()    
            impy.columns(1) 
                
            if impy.button("Some button"):  
                a = 0   
                print("!!!")    
                    
            impy.progress_bar(a)    
                
            impy.combo("Combo!", selectedItem, mylist)  
                
            impy.push_item_width(-10.0) 
            impy.plot_lines("Some plot", vals, graph_size = impy.Vec2(0, 300))  
            impy.pop_item_width()   
            
            a += 0.01
        impy.end()
    
    ctx.render()
