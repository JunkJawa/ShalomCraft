package com.shalomcraft;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;

/** A food that is drunk or spooned from a bowl and gives the bowl back (set via the food's usingConvertsTo). */
public class BowlFoodItem extends Item {
    public BowlFoodItem(Properties properties) {
        super(properties);
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.DRINK;
    }
}
