package com.shalomcraft;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(ShalomCraft.MODID);

    public static final DeferredBlock<Block> MENORAH = BLOCKS.register("menorah",
            () -> new MenorahBlock(BlockBehaviour.Properties.of()
                    .strength(1.0f)
                    .sound(SoundType.METAL)
                    .noOcclusion()));
}
