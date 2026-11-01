package com.shalomcraft;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.goat.Goat;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

/** Gameplay hooks that are not tied to one item. */
@EventBusSubscriber(modid = ShalomCraft.MODID)
public class ModEvents {
    /** How long a goat needs before its hide can be sheared again, in ticks (5 minutes). */
    private static final long HIDE_REGROW_TICKS = 6000;
    private static final String LAST_SHEARED = "ShalomLastSheared";

    private static final TagKey<Item> SHEARS_TOOLS = TagKey.create(Registries.ITEM,
            ResourceLocation.fromNamespaceAndPath("c", "tools/shear"));
    private static final TagKey<Item> SHEARS_LEGACY = TagKey.create(Registries.ITEM,
            ResourceLocation.fromNamespaceAndPath("c", "shears"));

    private static boolean isShears(ItemStack stack) {
        return stack.is(Items.SHEARS) || stack.is(SHEARS_TOOLS) || stack.is(SHEARS_LEGACY);
    }

    /** Shears on an adult goat give a hide. The goat is not hurt, and its hide grows back over time. */
    @SubscribeEvent
    public static void onGoatInteract(PlayerInteractEvent.EntityInteract event) {
        if (!(event.getTarget() instanceof Goat goat) || goat.isBaby()) return;
        ItemStack held = event.getItemStack();
        if (!isShears(held)) return;

        Level level = event.getLevel();
        Player player = event.getEntity();
        event.setCancellationResult(InteractionResult.sidedSuccess(level.isClientSide));
        event.setCanceled(true);
        if (level.isClientSide) return;

        long now = level.getGameTime();
        long last = goat.getPersistentData().contains(LAST_SHEARED) ? goat.getPersistentData().getLong(LAST_SHEARED) : -HIDE_REGROW_TICKS;
        if (now - last < HIDE_REGROW_TICKS) {
            player.displayClientMessage(Component.translatable("message.shalomcraft.goat_hide_growing"), true);
            return;
        }
        goat.getPersistentData().putLong(LAST_SHEARED, now);
        level.playSound(null, goat.blockPosition(), SoundEvents.SHEEP_SHEAR, SoundSource.PLAYERS, 1.0F, 1.0F);
        goat.spawnAtLocation(new ItemStack(ModItems.GOAT_HIDE.get(), 1 + level.getRandom().nextInt(2)));
        if (!player.getAbilities().instabuild) {
            held.hurtAndBreak(1, player, LivingEntity.getSlotForHand(event.getHand()));
        }
        goat.gameEvent(GameEvent.SHEAR, player);
    }
}
