package com.shalomcraft;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A mezuzah mounted on the side of a block, tilted. FACING is the way it faces out from the wall.
 * Right click with an empty hand to flip which way the top leans.
 */
public class MezuzahBlock extends HorizontalDirectionalBlock {
    public static final MapCodec<MezuzahBlock> CODEC = simpleCodec(MezuzahBlock::new);
    public static final BooleanProperty FLIPPED = BooleanProperty.create("flipped");

    private static final VoxelShape ON_NORTH_WALL = Block.box(3, 1, 0, 13, 15, 2);   // faces south
    private static final VoxelShape ON_SOUTH_WALL = Block.box(3, 1, 14, 13, 15, 16); // faces north
    private static final VoxelShape ON_WEST_WALL = Block.box(0, 1, 3, 2, 15, 13);    // faces east
    private static final VoxelShape ON_EAST_WALL = Block.box(14, 1, 3, 16, 15, 13);  // faces west

    public MezuzahBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.SOUTH).setValue(FLIPPED, false));
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
        return CODEC;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, FLIPPED);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        Direction clicked = context.getClickedFace();
        if (clicked.getAxis().isHorizontal()) {
            BlockState state = defaultBlockState().setValue(FACING, clicked);
            if (state.canSurvive(context.getLevel(), context.getClickedPos())) return state;
        }
        for (Direction dir : context.getNearestLookingDirections()) {
            if (!dir.getAxis().isHorizontal()) continue;
            BlockState state = defaultBlockState().setValue(FACING, dir.getOpposite());
            if (state.canSurvive(context.getLevel(), context.getClickedPos())) return state;
        }
        return null;
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        Direction facing = state.getValue(FACING);
        BlockPos wall = pos.relative(facing.getOpposite());
        return level.getBlockState(wall).isFaceSturdy(level, wall, facing);
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (direction == state.getValue(FACING).getOpposite() && !state.canSurvive(level, pos)) {
            return Blocks.AIR.defaultBlockState();
        }
        return super.updateShape(state, direction, neighborState, level, pos, neighborPos);
    }

    /** Empty hand flips the slant, so the top can lean into the room from either side of a doorway. */
    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player,
                                               BlockHitResult hit) {
        if (!player.getMainHandItem().isEmpty()) return InteractionResult.PASS;
        if (!level.isClientSide) {
            level.setBlock(pos, state.cycle(FLIPPED), Block.UPDATE_ALL);
            level.playSound(null, pos, SoundEvents.ITEM_FRAME_ROTATE_ITEM, SoundSource.BLOCKS, 1.0F, 1.0F);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return switch (state.getValue(FACING)) {
            case SOUTH -> ON_NORTH_WALL;
            case NORTH -> ON_SOUTH_WALL;
            case EAST -> ON_WEST_WALL;
            default -> ON_EAST_WALL;
        };
    }
}
