def cmd_give(target, type_, amount):
    target.inventory.addItem(int(type_), int(amount))


cmd_dict = {
    "give": cmd_give
}