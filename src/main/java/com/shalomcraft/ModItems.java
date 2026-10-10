package com.shalomcraft;

import java.util.function.Supplier;

import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.BannerPatternItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ShalomCraft.MODID);

    /** Looks up a Farmer's Delight effect by id at eating time, with a vanilla fallback. */
    private static Supplier<MobEffectInstance> fdEffect(String path, int ticks, Holder<MobEffect> fallback) {
        return () -> {
            Holder<MobEffect> holder = BuiltInRegistries.MOB_EFFECT
                    .getHolder(ResourceLocation.fromNamespaceAndPath("farmersdelight", path))
                    .<Holder<MobEffect>>map(ref -> ref)
                    .orElse(fallback);
            return new MobEffectInstance(holder, ticks, 0);
        };
    }

    private static Supplier<MobEffectInstance> effect(Holder<MobEffect> effect, int ticks, int amplifier) {
        return () -> new MobEffectInstance(effect, ticks, amplifier);
    }

    private static FoodProperties.Builder food(int nutrition, float saturation) {
        return new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation);
    }

    private static DeferredItem<Item> plain(String name) {
        return ITEMS.registerSimpleItem(name, new Item.Properties());
    }

    private static DeferredItem<Item> edible(String name, FoodProperties.Builder food) {
        return ITEMS.registerSimpleItem(name, new Item.Properties().food(food.build()));
    }

    // Ingredients
    public static final DeferredItem<Item> CHALLAH_DOUGH = plain("challah_dough");
    public static final DeferredItem<Item> BAGEL_DOUGH = plain("bagel_dough");
    public static final DeferredItem<Item> RAW_LATKE = plain("raw_latke");
    public static final DeferredItem<Item> CREAM_CHEESE = plain("cream_cheese");
    public static final DeferredItem<Item> LOX = edible("lox", food(3, 0.4f));

    // Foods
    public static final DeferredItem<Item> CHALLAH = edible("challah", food(8, 0.7f)
            .effect(fdEffect("nourishment", 1200, MobEffects.SATURATION), 1.0f));

    public static final DeferredItem<Item> LATKE = edible("latke", food(6, 0.6f));

    public static final DeferredItem<Item> MATZO = edible("matzo", food(4, 0.4f));

    public static final DeferredItem<Item> MATZO_BALL_SOUP = ITEMS.registerItem("matzo_ball_soup",
            BowlFoodItem::new,
            new Item.Properties().stacksTo(16).food(food(12, 0.75f)
                    .usingConvertsTo(Items.BOWL)
                    .effect(fdEffect("comfort", 3600, MobEffects.REGENERATION), 1.0f)
                    .effect(fdEffect("nourishment", 3600, MobEffects.SATURATION), 1.0f)
                    .build()));

    public static final DeferredItem<Item> GEFILTE_FISH = edible("gefilte_fish", food(8, 0.7f)
            .effect(effect(MobEffects.WATER_BREATHING, 600, 0), 0.5f));

    public static final DeferredItem<Item> RUGELACH = edible("rugelach", food(4, 0.5f)
            .effect(effect(MobEffects.MOVEMENT_SPEED, 400, 0), 0.5f));

    public static final DeferredItem<Item> BABKA = edible("babka", food(10, 1.0f)
            .effect(fdEffect("nourishment", 4800, MobEffects.SATURATION), 1.0f)
            .effect(effect(MobEffects.REGENERATION, 200, 1), 1.0f)
            .effect(effect(MobEffects.ABSORPTION, 2400, 1), 1.0f));

    public static final DeferredItem<Item> GELT = edible("gelt", food(2, 0.3f).fast());

    public static final DeferredItem<Item> AFIKOMEN = edible("afikomen", food(8, 1.0f)
            .effect(effect(MobEffects.REGENERATION, 300, 1), 1.0f)
            .effect(effect(MobEffects.DAMAGE_RESISTANCE, 1200, 0), 1.0f)
            .effect(fdEffect("nourishment", 3600, MobEffects.SATURATION), 1.0f));

    // Bagels
    public static final DeferredItem<Item> BAGEL = edible("bagel", food(5, 0.5f));
    public static final DeferredItem<Item> BAGEL_WITH_CREAM_CHEESE = edible("bagel_with_cream_cheese", food(7, 0.6f));
    public static final DeferredItem<Item> BAGEL_WITH_LOX = edible("bagel_with_lox", food(8, 0.7f));
    public static final DeferredItem<Item> BAGEL_WITH_LOX_AND_CREAM_CHEESE =
            edible("bagel_with_lox_and_cream_cheese", food(11, 0.85f)
                    .effect(fdEffect("nourishment", 2400, MobEffects.SATURATION), 1.0f));

    // Worn items: dyeable, no protection
    public static final DeferredItem<Item> KIPPAH = ITEMS.register("kippah",
            () -> new ArmorItem(ModArmorMaterials.CLOTH, ArmorItem.Type.HELMET, new Item.Properties().stacksTo(1)));
    public static final DeferredItem<Item> TALLIT = ITEMS.register("tallit",
            () -> new ArmorItem(ModArmorMaterials.CLOTH, ArmorItem.Type.CHESTPLATE, new Item.Properties().stacksTo(1)));

    // Banner pattern for the loom
    public static final DeferredItem<Item> STAR_OF_DAVID_BANNER_PATTERN = ITEMS.register("star_of_david_banner_pattern",
            () -> new BannerPatternItem(
                    TagKey.create(Registries.BANNER_PATTERN,
                            ResourceLocation.fromNamespaceAndPath(ShalomCraft.MODID, "pattern_item/star_of_david")),
                    new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON)));

    // Blocks
    public static final DeferredItem<BlockItem> MENORAH = ITEMS.registerSimpleBlockItem("menorah", ModBlocks.MENORAH);
}
