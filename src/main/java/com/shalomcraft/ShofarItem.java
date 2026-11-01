package com.shalomcraft;

import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;

/** A shofar made from a goat horn. Blows a long blast that carries a long way. */
public class ShofarItem extends Item {
    public static final int BLAST_TICKS = 100;

    public ShofarItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.startUsingItem(hand);
        if (!level.isClientSide) {
            level.playSound(null, player, ModSounds.SHOFAR.get(), SoundSource.PLAYERS, 6.0F, 1.0F);
            level.gameEvent(player, GameEvent.INSTRUMENT_PLAY, player.position());
        }
        player.getCooldowns().addCooldown(this, BLAST_TICKS + 40);
        return InteractionResultHolder.consume(stack);
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.TOOT_HORN;
    }

    @Override
    public int getUseDuration(ItemStack stack, LivingEntity entity) {
        return BLAST_TICKS;
    }
}
