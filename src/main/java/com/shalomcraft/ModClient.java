package com.shalomcraft;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.FastColor;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.DyedItemColor;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
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

    /**
     * Drives the dreidel animation. While the dreidel is on cooldown (spinning) this returns 0.1, 0.3, 0.5 or 0.7,
     * cycling fast at first and slowing down, and the item model picks a spin frame from that. At rest it returns 0.
     */
    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> ItemProperties.register(ModItems.DREIDEL.get(),
                ResourceLocation.fromNamespaceAndPath(ShalomCraft.MODID, "spin"),
                (stack, level, entity, seed) -> {
                    LivingEntity holder = entity != null ? entity : Minecraft.getInstance().player;
                    if (!(holder instanceof Player player)) return 0.0F;
                    float remaining = player.getCooldowns().getCooldownPercent(stack.getItem(), 0.0F);
                    if (remaining <= 0.0F) return 0.0F;
                    float elapsed = 1.0F - remaining;
                    int phase = (int) (Math.sqrt(elapsed) * 30.0F) % 4;
                    return 0.1F + 0.2F * phase;
                }));
    }
}
