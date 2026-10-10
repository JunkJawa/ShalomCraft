package com.shalomcraft;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(ShalomCraft.MODID);

    private static BlockBehaviour.Properties metal() {
        return BlockBehaviour.Properties.of().strength(1.0f).sound(SoundType.METAL).noOcclusion();
    }

    private static BlockBehaviour.Properties wallPiece() {
        return BlockBehaviour.Properties.of().strength(0.5f).sound(SoundType.METAL).noOcclusion().noCollission()
                .pushReaction(PushReaction.DESTROY);
    }

    public static final DeferredBlock<Block> MENORAH = BLOCKS.register("menorah",
            () -> new MenorahBlock(metal().lightLevel(MenorahBlock::lightLevel)));

    public static final DeferredBlock<Block> GOLD_CANDLESTICKS = BLOCKS.register("gold_candlesticks",
            () -> new CandlesticksBlock(metal().lightLevel(CandlesticksBlock::lightLevel)));
    public static final DeferredBlock<Block> SILVER_CANDLESTICKS = BLOCKS.register("silver_candlesticks",
            () -> new CandlesticksBlock(metal().lightLevel(CandlesticksBlock::lightLevel)));

    public static final DeferredBlock<Block> GOLD_MEZUZAH = BLOCKS.register("gold_mezuzah",
            () -> new MezuzahBlock(wallPiece()));
    public static final DeferredBlock<Block> SILVER_MEZUZAH = BLOCKS.register("silver_mezuzah",
            () -> new MezuzahBlock(wallPiece()));
}
