from stages.pg_utils import load_image
class InventoryItem:
    def icon():
        return None

    def use(hero):
        return False

class InventoryItemFood(InventoryItem):
    def icon():
        return load_image('items/food_icon.png')
    def use(hero):
        hero.HP += 1
        if hero.HP > hero.MAX_HP: 
            hero.HP = hero.MAX_HP
        return True

types = [
    InventoryItem,
    InventoryItemFood
]