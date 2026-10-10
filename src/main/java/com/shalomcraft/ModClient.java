package com.shalomcraft;

import net.minecraft.util.FastColor;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.DyedItemColor;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;

/** Client only setup: dye tinting for the kippah and tallit. */
@EventBusSubscriber(modid = ShalomCraft.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ModClient {
    private static final int UNDYED = 0xFFFFFF;

    /** Tints the first item layer (the cloth) by the dye colour, leaves the overlay layer alone. */
    @SubscribeEvent
    public static void itemColors(RegisterColorHandlersEvent.Item event) {
        event.register(
                (stack, tintIndex) -> tintIndex == 0
                        ? FastColor.ARGB32.opaque(DyedItemColor.getOrDefault(stack, UNDYED))
                        : -1,
                ModItems.KIPPAH.get(), ModItems.TALLIT.get());
    }

    /** Undyed worn cloth should render white, not leather brown. */
    @SubscribeEvent
    public static void clientExtensions(RegisterClientExtensionsEvent event) {
        event.registerItem(new IClientItemExtensions() {
            @Override
            public int getDefaultDyeColor(ItemStack stack) {
                return 0xFFFFFFFF;
            }
        }, ModItems.KIPPAH.get(), ModItems.TALLIT.get());
    }
}
