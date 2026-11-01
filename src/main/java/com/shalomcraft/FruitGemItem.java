package com.shalomcraft;

import java.util.List;

import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/** Sugar coated fruit jelly. Eating one gives a random good effect. */
public class FruitGemItem extends Item {

    /** One entry of the prize pool: the effect, how long it lasts in ticks, and its level (0 is level one). */
    private record Prize(Holder<MobEffect> effect, int ticks, int amplifier) {}

    private static final List<Prize> PRIZES = List.of(
            new Prize(MobEffects.MOVEMENT_SPEED, 900, 0),
            new Prize(MobEffects.DIG_SPEED, 900, 0),
            new Prize(MobEffects.JUMP, 900, 1),
            new Prize(MobEffects.REGENERATION, 160, 0),
            new Prize(MobEffects.NIGHT_VISION, 1800, 0),
            new Prize(MobEffects.ABSORPTION, 1200, 0),
            new Prize(MobEffects.LUCK, 3600, 0),
            new Prize(MobEffects.SLOW_FALLING, 900, 0),
            new Prize(MobEffects.WATER_BREATHING, 1200, 0),
            new Prize(MobEffects.FIRE_RESISTANCE, 1200, 0),
            new Prize(MobEffects.DAMAGE_RESISTANCE, 400, 0),
            new Prize(MobEffects.DAMAGE_BOOST, 400, 0),
            new Prize(MobEffects.DOLPHINS_GRACE, 900, 0),
            new Prize(MobEffects.HEALTH_BOOST, 1200, 0));

    public FruitGemItem(Properties properties) {
        super(properties);
    }

    @Override
    public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity entity) {
        ItemStack result = super.finishUsingItem(stack, level, entity);
        if (!level.isClientSide) {
            Prize prize = PRIZES.get(entity.getRandom().nextInt(PRIZES.size()));
            entity.addEffect(new MobEffectInstance(prize.effect(), prize.ticks(), prize.amplifier()));
            if (entity instanceof Player player) {
                player.displayClientMessage(Component.translatable("item.shalomcraft.fruit_gem.effect",
                        prize.effect().value().getDisplayName()), true);
            }
        }
        return result;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.shalomcraft.fruit_gem.tooltip")
                .withStyle(net.minecraft.ChatFormatting.GRAY));
    }
}
