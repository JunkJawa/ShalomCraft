package com.shalomcraft;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.Vec3;

/** Shared lighting and geometry helpers for the menorah and the Shabbat candlesticks. */
public final class Candles {
    /** Anything in this tag can light a candle. Add modded lighters with a data pack. */
    public static final TagKey<Item> LIGHTERS =
            TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(ShalomCraft.MODID, "candle_lighters"));

    private Candles() {}

    public static boolean isLighter(ItemStack stack) {
        return stack.is(LIGHTERS);
    }

    /** Uses up a flint and steel durability point, or one fire charge. Creative players keep their item. */
    private static void consume(ItemStack stack, Player player, InteractionHand hand) {
        if (player.getAbilities().instabuild) return;
        if (stack.isDamageableItem()) {
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        } else {
            stack.shrink(1);
        }
    }

    /** Lights candle {@code prop} if the player holds a lighter and the candle is not lit yet. */
    public static ItemInteractionResult tryLight(ItemStack stack, Level level, BlockPos pos, BlockState state,
                                                 BooleanProperty prop, Player player, InteractionHand hand) {
        if (!isLighter(stack) || state.getValue(prop)) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        if (!level.isClientSide) {
            level.setBlock(pos, state.setValue(prop, true), Block.UPDATE_ALL);
            level.playSound(null, pos,
                    stack.is(Items.FIRE_CHARGE) ? SoundEvents.FIRECHARGE_USE : SoundEvents.FLINTANDSTEEL_USE,
                    SoundSource.BLOCKS, 1.0F, level.getRandom().nextFloat() * 0.4F + 0.8F);
            level.gameEvent(player, GameEvent.BLOCK_CHANGE, pos);
            consume(stack, player, hand);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }

    /** Puts out candle {@code prop} when clicked with an empty hand. */
    public static InteractionResult trySnuff(Level level, BlockPos pos, BlockState state, BooleanProperty prop,
                                             Player player) {
        if (!player.getMainHandItem().isEmpty() || !state.getValue(prop)) {
            return InteractionResult.PASS;
        }
        if (!level.isClientSide) {
            level.setBlock(pos, state.setValue(prop, false), Block.UPDATE_ALL);
            level.playSound(null, pos, SoundEvents.CANDLE_EXTINGUISH, SoundSource.BLOCKS, 1.0F, 1.0F);
            level.gameEvent(player, GameEvent.BLOCK_CHANGE, pos);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    /**
     * Where a point given in model coordinates (16 units per block, model drawn facing north) ends up
     * in the block after the blockstate rotates it to {@code facing}. Returns block fractions 0..1.
     */
    public static Vec3 toBlock(Direction facing, double xm, double ym, double zm) {
        return switch (facing) {
            case SOUTH -> new Vec3((16 - xm) / 16, ym / 16, (16 - zm) / 16);
            case EAST -> new Vec3((16 - zm) / 16, ym / 16, xm / 16);
            case WEST -> new Vec3(zm / 16, ym / 16, (16 - xm) / 16);
            default -> new Vec3(xm / 16, ym / 16, zm / 16);
        };
    }

    /** The inverse for the long axis: the model x coordinate of a point inside the block (fractions 0..1). */
    public static double modelX(Direction facing, Vec3 local) {
        return switch (facing) {
            case SOUTH -> (1 - local.x) * 16;
            case EAST -> local.z * 16;
            case WEST -> (1 - local.z) * 16;
            default -> local.x * 16;
        };
    }
}
