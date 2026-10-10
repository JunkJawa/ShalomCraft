package com.shalomcraft;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ShalomCraft.MODID);

    public static final net.neoforged.neoforge.registries.DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN =
            TABS.register("main", () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.shalomcraft"))
                    .icon(() -> new ItemStack(ModItems.MENORAH.get()))
                    .displayItems((params, output) ->
                            ModItems.ITEMS.getEntries().forEach(entry -> output.accept(entry.get())))
                    .build());
}
