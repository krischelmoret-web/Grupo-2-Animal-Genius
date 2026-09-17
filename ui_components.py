import pygame

def crear_etiqueta_glossy(texto: str, fuente: pygame.font.Font, color_arriba: tuple, color_abajo: tuple) -> pygame.Surface:
    """Genera una placa estilo cápsula/píldora con degradado vertical, brillo glossy y contorno blanco."""
    txt_surf = fuente.render(texto, True, (255, 255, 255))
    tw, th = txt_surf.get_size()

    pad_x, pad_y = 22, 8
    w = tw + pad_x * 2
    h = th + pad_y * 2

    badge = pygame.Surface((w, h), pygame.SRCALPHA)

    # Degradado base
    grad_1x2 = pygame.Surface((1, 2), pygame.SRCALPHA)
    grad_1x2.set_at((0, 0), (*color_arriba, 255))
    grad_1x2.set_at((0, 1), (*color_abajo, 255))
    grad_surf = pygame.transform.smoothscale(grad_1x2, (w, h))

    # Máscara para bordes redondeados
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=h // 2)

    grad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    badge.blit(grad_surf, (0, 0))

    # Efecto de brillo (glossy) superior
    brillo = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(brillo, (255, 255, 255, 110), (4, 2, w - 8, h // 2))
    brillo.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    badge.blit(brillo, (0, 0))

    # Borde exterior
    pygame.draw.rect(badge, (255, 255, 255), (0, 0, w, h), width=4, border_radius=h // 2)

    # Texto con sombra
    sombra = fuente.render(texto, True, (0, 0, 0, 120))
    badge.blit(sombra, (pad_x + 1, pad_y + 2))
    badge.blit(txt_surf, (pad_x, pad_y))

    return badge


def crear_boton_glossy(
    texto: str, 
    fuente: pygame.font.Font, 
    ancho: int, 
    alto: int, 
    color_arriba: tuple = (100, 200, 255), 
    color_abajo: tuple = (30, 100, 200)
) -> pygame.Surface:
    """Genera un botón con forma de píldora, degradado lineal, efecto bisel y texto."""
    btn = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    # Degradado base
    grad_1x2 = pygame.Surface((1, 2), pygame.SRCALPHA)
    grad_1x2.set_at((0, 0), (*color_arriba, 255))
    grad_1x2.set_at((0, 1), (*color_abajo, 255))
    grad_surf = pygame.transform.smoothscale(grad_1x2, (ancho, alto))

    # Máscara para bordes redondeados
    mask = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, ancho, alto), border_radius=alto // 2)

    grad_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    btn.blit(grad_surf, (0, 0))

    # Efecto de brillo (glossy)
    brillo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.ellipse(brillo, (255, 255, 255, 100), (6, 2, ancho - 12, alto // 2))
    brillo.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    btn.blit(brillo, (0, 0))

    # Borde exterior
    pygame.draw.rect(btn, (255, 255, 255), (0, 0, ancho, alto), width=3, border_radius=alto // 2)

    # Texto centrado con sombra
    txt_surf = fuente.render(texto, True, (255, 255, 255))
    sombra = fuente.render(texto, True, (0, 0, 0))
    sombra.set_alpha(120)
    t_rect = txt_surf.get_rect(center=(ancho // 2, alto // 2))

    btn.blit(sombra, (t_rect.x + 1, t_rect.y + 2))
    btn.blit(txt_surf, t_rect)

    return btn


def dibujar_indicadores_progreso(
    pantalla: pygame.Surface, 
    x_centro: int, 
    y: int, 
    total_preguntas: int, 
    resultados: list[str],
    radio: int = 10,
    espacio: int = 30
) -> None:
    """
    Dibuja una barra de progreso horizontal con círculos (acierto/fallo/pendiente).
    
    :param pantalla: La superficie donde se dibujará.
    :param x_centro: El punto central en el eje X donde se alineará la barra completa.
    :param y: La posición en el eje Y.
    :param total_preguntas: Cantidad total de círculos a dibujar.
    :param resultados: Lista con cadenas ("acierto", "fallo") de las rondas completadas.
    """
    ancho_total = (total_preguntas * espacio) - (espacio - (radio * 2))
    inicio_x = x_centro - (ancho_total // 2)

    for i in range(total_preguntas):
        x = inicio_x + (i * espacio)
        estado = resultados[i] if i < len(resultados) else "pendiente"

        if estado == "acierto":
            color_relleno = (76, 175, 80)
            color_borde = (56, 142, 60)
        elif estado == "fallo":
            color_relleno = (244, 67, 54)
            color_borde = (198, 40, 40)
        else: # pendiente
            color_relleno = (255, 255, 255)
            color_borde = (76, 175, 80)

        # Dibujar relleno y luego el borde
        pygame.draw.circle(pantalla, color_relleno, (x, y), radio)
        pygame.draw.circle(pantalla, color_borde, (x, y), radio, width=2)

def aplicar_marco_capsula(
    imagen: pygame.Surface, 
                radio_borde: int = 25, 
                grosor_borde: int = 4, 
                color_borde: tuple = (255, 255, 255)
            ) -> pygame.Surface:
                """Recorta una imagen con bordes redondeados y le añade un borde perimetral."""
                ancho, alto = imagen.get_size()
                superficie_final = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            
                # 1. Crear máscara con bordes redondeados
                mascara = pygame.Surface((ancho, alto), pygame.SRCALPHA)
                pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, ancho, alto), border_radius=radio_borde)
            
                # 2. Aplicar máscara a la imagen
                superficie_final.blit(imagen, (0, 0))
                superficie_final.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            
                # 3. Dibujar borde redondeado
                pygame.draw.rect(superficie_final, color_borde, (0, 0, ancho, alto), width=grosor_borde, border_radius=radio_borde)
            
                return superficie_final
