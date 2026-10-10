package com.shalomcraft;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
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
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Nine branch hanukkiah. Each candle is lit on its own with flint and steel or a fire charge. */
public class MenorahBlock extends HorizontalDirectionalBlock {
    public static final MapCodec<MenorahBlock> CODEC = simpleCodec(MenorahBlock::new);

    public static final int CANDLES = 9;
    public static final int SHAMASH = 4;   // the taller helper candle in the middle
    public static final BooleanProperty[] LIT = new BooleanProperty[CANDLES];
    static {
        for (int i = 0; i < CANDLES; i++) LIT[i] = BooleanProperty.create("lit_" + i);
    }

    // Long side runs east to west when facing north or south
    private static final VoxelShape WIDE_X = Block.box(0, 0, 6, 16, 12, 10);
    private static final VoxelShape WIDE_Z = Block.box(6, 0, 0, 10, 12, 16);

    public MenorahBlock(Properties properties) {
        super(properties);
        BlockState state = stateDefinition.any().setValue(FACING, Direction.NORTH);
        for (BooleanProperty lit : LIT) state = state.setValue(lit, false);
        registerDefaultState(state);
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
        return CODEC;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING);
        builder.add(LIT);
    }

    /** Light level grows with the number of lit candles. */
    public static int lightLevel(BlockState state) {
        int lit = 0;
        for (BooleanProperty p : LIT) if (state.getValue(p)) lit++;
        return lit == 0 ? 0 : Math.min(15, 4 + lit * 2);
    }

    private static double candleX(int i) {
        return 2.0 + i * 1.5;
    }

    private static double candleTop(int i) {
        return i == SHAMASH ? 11.0 : 8.0;
    }

    private static int candleAt(BlockState state, BlockPos pos, BlockHitResult hit) {
        Vec3 local = hit.getLocation().subtract(pos.getX(), pos.getY(), pos.getZ());
        double xm = Candles.modelX(state.getValue(FACING), local);
        return Mth.clamp((int) Math.round((xm - 2.0) / 1.5), 0, CANDLES - 1);
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos,
                                              Player player, InteractionHand hand, BlockHitResult hit) {
        return Candles.tryLight(stack, level, pos, state, LIT[candleAt(state, pos, hit)], player, hand);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player,
                                               BlockHitResult hit) {
        return Candles.trySnuff(level, pos, state, LIT[candleAt(state, pos, hit)], player);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        Direction facing = state.getValue(FACING);
        for (int i = 0; i < CANDLES; i++) {
            if (!state.getValue(LIT[i])) continue;
            Vec3 p = Candles.toBlock(facing, candleX(i), candleTop(i) + 2.5, 8.0);
            level.addParticle(ParticleTypes.SMALL_FLAME, pos.getX() + p.x, pos.getY() + p.y, pos.getZ() + p.z, 0, 0, 0);
            if (random.nextInt(12) == 0) {
                level.addParticle(ParticleTypes.SMOKE, pos.getX() + p.x, pos.getY() + p.y + 0.05, pos.getZ() + p.z, 0, 0.01, 0);
            }
        }
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        return Block.canSupportCenter(level, pos.below(), Direction.UP);
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (direction == Direction.DOWN && !state.canSurvive(level, pos)) return Blocks.AIR.defaultBlockState();
        return super.updateShape(state, direction, neighborState, level, pos, neighborPos);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return state.getValue(FACING).getAxis() == Direction.Axis.Z ? WIDE_X : WIDE_Z;
    }
}
