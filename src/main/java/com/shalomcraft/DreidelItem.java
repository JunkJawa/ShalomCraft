package com.shalomcraft;

import java.util.List;

import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;

/**
 * A spinnable dreidel. Right click spins it, the item animates while it spins (see ModClient), and when it
 * stops it lands on one of the four letters and tells everyone nearby.
 */
public class DreidelItem extends Item {
    public static final int SPIN_TICKS = 50;
    private static final String[] LETTERS = { "nun", "gimel", "hay", "shin" };

    public DreidelItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.fail(stack);
        }
        if (!level.isClientSide) {
            int letter = level.getRandom().nextInt(LETTERS.length);
            long revealAt = level.getGameTime() + SPIN_TICKS;
            CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> {
                tag.putLong("RevealAt", revealAt);
                tag.putInt("Letter", letter);
            });
            level.playSound(null, player.blockPosition(), SoundEvents.ITEM_FRAME_ROTATE_ITEM, SoundSource.PLAYERS,
                    1.0F, 1.5F);
        }
        player.getCooldowns().addCooldown(this, SPIN_TICKS);
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** Waits for the spin to finish, then announces where it landed. Runs on the server for items in an inventory. */
    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        if (level.isClientSide || !(entity instanceof Player player)) return;
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        if (data == null) return;
        CompoundTag tag = data.copyTag();
        if (!tag.contains("RevealAt") || level.getGameTime() < tag.getLong("RevealAt")) return;

        int letter = Math.floorMod(tag.getInt("Letter"), LETTERS.length);
        tag.remove("RevealAt");
        tag.remove("Letter");
        if (tag.isEmpty()) stack.remove(DataComponents.CUSTOM_DATA);
        else stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));

        Component message = Component.translatable("item.shalomcraft.dreidel." + LETTERS[letter],
                player.getDisplayName()).withStyle(ChatFormatting.GOLD);
        level.playSound(null, player.blockPosition(), SoundEvents.ITEM_FRAME_PLACE, SoundSource.PLAYERS, 1.0F, 1.2F);
        for (Player nearby : level.getEntitiesOfClass(Player.class, player.getBoundingBox().inflate(10.0))) {
            nearby.sendSystemMessage(message);
        }
        player.displayClientMessage(Component.translatable("item.shalomcraft.dreidel.letter." + LETTERS[letter]), true);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.shalomcraft.dreidel.tooltip").withStyle(ChatFormatting.GRAY));
    }
}
