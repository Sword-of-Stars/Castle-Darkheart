
def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r.rect):
            hit_list.append(r)
    return hit_list