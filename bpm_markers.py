import bpy

bl_info = {
    "name": "BPM Timeline Markers",
    "author": "lebed.3d",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar > BPM | Timeline > Sidebar",
    "description": "Автоматическая расстановка маркеров по BPM",
    "category": "Animation",
}

class BPM_Properties(bpy.types.PropertyGroup):
    bpm: bpy.props.FloatProperty(name="BPM", default=120.0, min=1.0)
    step: bpy.props.FloatProperty(name="Шаг (в битах)", default=1.0, min=0.1)
    clear_existing: bpy.props.BoolProperty(name="Очистить старые", default=True)

class BPM_OT_GenerateMarkers(bpy.types.Operator):
    bl_idname = "bpm.generate_markers"
    bl_label = "Создать маркеры"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        props = scene.bpm_tool
        
        if props.clear_existing:
            scene.timeline_markers.clear()
        
        fps = scene.render.fps / scene.render.fps_base
        # Интервал между маркерами в кадрах
        interval = (60.0 / props.bpm) * fps * props.step
        current_frame = scene.frame_start
        count = 1
        
        while current_frame <= scene.frame_end:
            name = f"Beat {count}"
            scene.timeline_markers.new(name, frame=round(current_frame))
            current_frame += interval
            count += 1
        
        self.report({'INFO'}, f"Готово! Создано {count - 1} маркеров")
        return {'FINISHED'}

def draw_bpm_ui(layout, context):
    props = context.scene.bpm_tool
    col = layout.column(align=True)
    col.prop(props, "bpm")
    col.prop(props, "step")
    col.prop(props, "clear_existing")
    layout.separator()
    layout.operator("bpm.generate_markers", icon='MARKER')

class BPM_PT_ViewportPanel(bpy.types.Panel):
    bl_label = "BPM Markers"
    bl_idname = "BPM_PT_ViewportPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BPM'
    
    def draw(self, context):
        draw_bpm_ui(self.layout, context)

class BPM_PT_TimelinePanel(bpy.types.Panel):
    bl_label = "BPM Markers"
    bl_idname = "BPM_PT_TimelinePanel"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'BPM'
    
    def draw(self, context):
        draw_bpm_ui(self.layout, context)

classes = [BPM_Properties, BPM_OT_GenerateMarkers, BPM_PT_ViewportPanel, BPM_PT_TimelinePanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bpm_tool = bpy.props.PointerProperty(type=BPM_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bpm_tool

if __name__ == "__main__":
    register()
