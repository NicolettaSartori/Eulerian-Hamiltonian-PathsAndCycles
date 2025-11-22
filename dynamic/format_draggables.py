import xml.etree.ElementTree as ET

def replace_draggables(root, start_char, num, id):
    draggables = root.find('.//draggables')
    if draggables is not None:
        for child in list(draggables):
            draggables.remove(child)

        for i in range(num):
            draggables.append(ET.fromstring(format_draggable(chr(ord(start_char) + i), id)))
            id += 1
    else:
        raise ValueError("<draggables> tag not found in the XML file.")


def format_draggable(name, id):
    return f'''<DNDVisibleZonesDraggable id="{id}">
    <variableName>{name}</variableName>
    <htmlContent>&lt;div&gt;{name}&lt;/div&gt;</htmlContent>
    <numberOfDraggables>1</numberOfDraggables>
    <infiniteDraggables>false</infiniteDraggables>
    <dndVisibleZonesStage reference="5"/>
</DNDVisibleZonesDraggable>
'''

