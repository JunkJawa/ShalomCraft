package com.shalomcraft;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(ShalomCraft.MODID)
public class ShalomCraft {
    public static final String MODID = "shalomcraft";

    public ShalomCraft(IEventBus modBus) {
        ModBlocks.BLOCKS.register(modBus);
        ModItems.ITEMS.register(modBus);
        ModCreativeTabs.TABS.register(modBus);
    }
}
