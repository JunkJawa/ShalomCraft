package com.shalomcraft;

import java.util.EnumMap;
import java.util.List;

import net.minecraft.Util;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Cloth worn items (kippah, tallit). No protection, just a dyeable look. */
public class ModArmorMaterials {
    public static final DeferredRegister<ArmorMaterial> MATERIALS =
            DeferredRegister.create(Registries.ARMOR_MATERIAL, ShalomCraft.MODID);

    public static final Holder<ArmorMaterial> CLOTH = MATERIALS.register("cloth", () -> {
        ResourceLocation texture = ResourceLocation.fromNamespaceAndPath(ShalomCraft.MODID, "cloth");
        return new ArmorMaterial(
                Util.make(new EnumMap<>(ArmorItem.Type.class), map -> {
                    map.put(ArmorItem.Type.BOOTS, 0);
                    map.put(ArmorItem.Type.LEGGINGS, 0);
                    map.put(ArmorItem.Type.CHESTPLATE, 0);
                    map.put(ArmorItem.Type.HELMET, 0);
                    map.put(ArmorItem.Type.BODY, 0);
                }),
                15,
                SoundEvents.ARMOR_EQUIP_LEATHER,
                () -> Ingredient.of(Items.STRING),
                // first layer is tinted by the dye colour, the overlay (stripes, trim, fringe) is not
                List.of(new ArmorMaterial.Layer(texture, "", true),
                        new ArmorMaterial.Layer(texture, "_overlay", false)),
                0.0F,
                0.0F);
    });
}
