"""Genera mapa_ecosistemico_interactivo.html: un único archivo HTML autocontenido (sin dependencias externas)."""
import json, base64, io
from PIL import Image

U = {  # fuentes
 'mincit': ('MinCIT, Decreto 636 de 2026', 'https://www.mincit.gov.co/prensa/noticias/comercio/gobierno-adopta-medidas-para-industria-vidrio'),
 'mincitpd': ('MinCIT, proyecto de decreto (2026)', 'https://www.mincit.gov.co/normatividad/proyectos-de-normatividad/proyectos-de-decreto-2026/06-05-2026-pd-incremento-arancel-vidrio.aspx'),
 'antid': ('MinCIT, investigación antidumping', 'https://www.mincit.gov.co/mincomercioexterior/defensa-comercial/dumping/investigaciones-antidumping-concluidas/vidrio-flotado-o-vidrio-incoloro-placas-o-en-hojas'),
 'camacol': ('Camacol, Informe Jurídico 1036', 'https://camacol.co/sites/default/files/descargables/INFORMEJURIDICO%201036_0.pdf'),
 'semana25': ('Semana (2025), Acolvise e importaciones', 'https://www.semana.com/economia/articulo/industria-nacional-del-vidrio-para-construccion-al-borde-de-la-desaparicion-expertos-claman-por-medidas-urgentes/202533/'),
 'acolvise': ('Acolvise, gestión', 'http://acolvise.org/inicio/gestion/'),
 'acolvisec': ('Acolvise, II Congreso de Sistemas Vidriados', 'http://acolvise.org/wp-content/uploads/2019/10/05-C95-Final-II-Congreso-de-sistemas-vidriados.pdf'),
 'peldar': ('MinCIT/PIGCCS, caso O-I Peldar', 'https://pigccs.mincit.gov.co/piggccs_mincit/media/pdf/20220706-Caso-Peldar.pdf'),
 'blu': ('Blu Radio, vidrio reciclado en el Valle de Aburrá', 'https://www.bluradio.com/medio-ambiente/recicladores-ya-no-saben-que-hacer-con-el-vidrio-que-recuperan-en-el-valle-de-aburra'),
 'dnp': ('DNP, cadena del vidrio', 'https://colaboracion.dnp.gov.co/cdt/desarrollo%20empresarial/vidrio.pdf'),
 'va': ('Vidrio Andino, quiénes somos', 'https://www.vidrioandino.com/quienes-somos'),
 'sgva': ('Saint-Gobain Colombia, Vidrio Andino', 'https://www.saint-gobain.com.co/vidrio-andino'),
 'lr19': ('La República (2019), planta de Galapa', 'https://www.larepublica.co/empresas/planta-de-tecnoglass-y-saint-gobain-sumara-750-toneladas-de-vidrio-al-dia-2814870'),
 'gi19': ('Glass International (2019)', 'https://www.glass-international.com/news/tecnoglass-plans-160-million-colombian-float-glass-plant'),
 'tg10k': ('Tecnoglass, Form 10-K 2025 (SEC)', 'https://www.sec.gov/Archives/edgar/data/1534675/000149315226008465/form10-k.htm'),
 'tgres': ('Tecnoglass, resultados 2025', 'https://www.globenewswire.com/news-release/2026/02/26/3245421/0/en/Tecnoglass-Reports-Fourth-Quarter-and-Full-Year-2025-Results.html'),
 'es5000': ('Ficha ES-5000 (instalador)', 'https://www.armorprowindows.com/manufacturers/eswindows/elite/es-5000'),
 'vidplex': ('Vidplex, Alto Desempeño', 'https://vidplex.com/en-us/high-performance/'),
 'agp': ('AGP Colombia', 'https://agpglass.com/es/col/sobre-sglass/'),
 'agpul': ('AGP, Ultra Light Glass', 'https://agpglass.com/col/veiculos-blindados-civis/ultra-light-glass/ultra-light-glass/'),
 'pat': ('Patentes de AGP America S.A. (Justia)', 'https://patents.justia.com/assignee/agp-america-s-a'),
 'sgsteel': ('Securitglass, Steel Glass', 'https://securitglass.com.co/steel-glass/'),
 'sgcert': ('Securitglass, certificaciones', 'https://securitglass.com.co/nuestras-certificaciones/'),
 'semanabl': ('Semana (2026), blindaje vehicular', 'https://www.semana.com/economia/capsulas/articulo/el-blindaje-vehicular-en-colombia-supera-los-277000-millones-y-el-renting-gana-espacio-con-neosecurity/202653/'),
 'lr22': ('La República (2022), blindaje', 'https://www.larepublica.co/especiales/seguridad-una-prioridad/las-empresas-de-blindaje-se-enfocan-en-usados-y-en-protecciones-mas-sencillas-3425647'),
 'sofasa': ('El Carro Colombiano, Sofasa 2025', 'https://www.elcarrocolombiano.com/industria/renault-sofasa-produccion-carros-colombia-exportaciones-2025/'),
 'veritrade': ('Veritrade, importaciones 7007.21', 'https://www.veritradecorp.com/es/colombia/importaciones-y-exportaciones-glass--laminados----templados--importaciones--sas/nit-900519083'),
 'ntc': ('ICONTEC, NTC 1578:2023', 'https://tienda.icontec.org/gp-ntc-vidrios-de-seguridad-utilizados-en-construcciones-especificaciones-y-metodos-de-ensayo-ntc1578-2023.html'),
 'sic': ('SIC, reglamento de acristalamientos', 'https://www.sic.gov.co/sites/default/files/documentos/Reglamento_AcristalamientoSeguridad_sinTABLA.pdf'),
 'gmi': ('GMI, mercado de vidrio inteligente', 'https://www.gminsights.com/industry-analysis/smart-glass-market'),
}

# id, x, y, w, h, tipo, sector(s), titulo, lineas, detalle, fuentes, diagrama
N = [
 ('g1', 45, 125, 290, 100, 'gre', 'arq', 'Acolvise (2004)', ['normalización, conocimiento,', 'defensa comercial; preside', 'un directivo de Vidplex'],
  'Asociación Colombiana de Sistemas Vidriados. Reúne transformadores y comercializadores de vidrio de seguridad, proveedores de insumos para cerramientos y fabricantes de ventanería. Trabaja en normalización, conocimiento y conexión entre empresas con ICONTEC, la SCA y el CCCS. Su interés principal es la defensa comercial frente a importaciones a bajo precio.', ['acolvise', 'semana25'], None),
 ('g2', 345, 125, 290, 100, 'gre', 'arq', 'Camacol · CCCS · SCA', ['construcción, edificación', 'sostenible e informes jurídicos'],
  'Camacol representa a los constructores, es decir, a los compradores de vidrio; por ende, en materia arancelaria su interés es el contrario al del productor primario. El CCCS impulsa la construcción sostenible y la SCA participa en la normalización con Acolvise.', ['camacol', 'acolvise'], None),
 ('g3', 645, 125, 290, 100, 'gre', 'aut', 'Acolfa · Andemos', ['autopartes, producción y', 'ventas de vehículos'],
  'Acolfa agrupa a los fabricantes de autopartes y Andemos a los importadores y vendedores de vehículos. Son la fuente de cifras de producción y ventas del sector automotriz.', ['sofasa'], None),
 ('g4', 945, 125, 290, 100, 'gov', 'all', 'MinCIT', ['Decreto 636/2026: arancel 35 %', 'antidumping sin derechos (2025)'],
  'Define la política comercial. La investigación antidumping al flotado chino terminó sin derechos (Res. 114 de 2025). Luego, el Decreto 636 del 26 de junio de 2026 subió del 10 % al 35 % el arancel al flotado incoloro (subpartidas 7005.29.10.00 y 7005.29.90.00) de países sin TLC por cinco años.', ['mincit', 'antid', 'camacol'], None),
 ('g5', 1245, 125, 290, 100, 'gov', 'all', 'ICONTEC · MinVivienda', ['NTC 1578, 1909, 4325, 1467', 'NSR-10, Título K'],
  'ICONTEC emite las normas técnicas: NTC 1578 (vidrio de seguridad en construcción), NTC 1909 (control solar), NTC 4325 (ventanas de aluminio) y NTC 1467 (vidrio de seguridad automotriz). La NSR-10, Título K, exige laminado en áreas de riesgo, pero no incorpora confort ni ahorro energético.', ['ntc', 'acolvisec'], None),
 ('g6', 1545, 125, 300, 100, 'gov', 'aut', 'Supervigilancia · SIC', ['blindaje vehicular autorizado;', 'reglamentos técnicos y patentes'],
  'Supervigilancia autoriza y regula a las empresas de blindaje. La SIC expide reglamentos técnicos (acristalamientos de seguridad automotriz) y administra el registro de patentes en Colombia.', ['sic', 'semanabl'], None),
 ('mp1', 40, 300, 280, 80, 'ins', 'all', 'Arena sílice, caliza, dolomita', ['minería nacional'],
  'Componentes principales del vidrio sodocálcico. Se extraen en Colombia y abastecen tanto al vidrio plano (Vidrio Andino) como a envases (O-I Peldar).', ['dnp'], None),
 ('mp2', 40, 400, 280, 70, 'ins', 'all', 'Carbonato de sodio', ['principalmente importado'],
  'Fundente que reduce la temperatura de fusión de la sílice. El calcín (vidrio reciclado) cumple una función similar y reduce el consumo de energía del horno.', ['dnp'], None),
 ('mp4', 40, 560, 280, 80, 'ins', 'arq', 'Perfiles de aluminio y PVC', ['Alutions (Tecnoglass), proveedores'],
  'Tecnoglass se integra verticalmente con Alutions, su filial de fundición y extrusión de aluminio (cerca de 4.100 t/mes), y con líneas propias de vinilo.', ['tg10k'], None),
 ('mp3', 40, 760, 280, 110, 'ins', 'all', 'Interlayers y polímeros', ['PVB, ionoplástico, policarbonato,', 'película PDLC/SPD', '(importados)'],
  'PVB e ionoplástico (SentryGlas) para laminado arquitectónico; policarbonato e interlayers de PU para blindaje; películas PDLC o SPD para vidrio inteligente. No se identificó fabricación local de ninguno de ellos.', ['tg10k'], None),
 ('va', 385, 325, 300, 140, 'pri', 'all', 'Vidrio Andino (Soacha)', ['única planta de flotado del país', 'Saint-Gobain + NSG; 25,8 % Tecnoglass', '≈200.000 t/año (estimado), 3–10 mm', 'Galapa duplicaría la producción'],
  'Única planta de vidrio flotado de Colombia, joint venture de Saint-Gobain y NSG Pilkington; Tecnoglass compró cerca del 25,8 % en 2019. Produce flotado incoloro y extra claro (SGG Diamant) de 3 a 10 mm y laminado SGG Stadip. Su web declara «±600 t al mes», lo cual se interpreta como t/día. No publica tipo de horno, % de calcín ni EPD. Calificación de innovación: 13/25 (adoptante de tecnología del grupo).', ['va', 'sgva', 'tg10k', 'lr19'], 'f1_vidrio_andino.png'),
 ('gal', 385, 485, 300, 90, 'unk', 'arq', 'Planta Galapa (Atlántico)', ['750 t/día, USD 160 M, anunciada', 'en 2019; estado sin confirmar'],
  'Segunda planta de flotado anunciada en 2019 junto con la entrada de Tecnoglass: 750 t/día, USD 160 M, prevista para 2021 y con vidrio de color. El 10-K de 2025 no reporta su entrada en operación.', ['gi19', 'lr19', 'tg10k'], None),
 ('oi', 385, 600, 300, 90, 'oth', 'none', 'O-I Peldar (envases)', ['Zipaquirá y Soacha; compra', 'calcín a recicladores'],
  'Principal fabricante de envases de vidrio. Cerca del 80 % del calcín que recibe lo recogen recicladores de oficio. El cierre de su planta de Envigado dejó sin comprador el vidrio reciclado del Valle de Aburrá.', ['peldar', 'blu'], None),
 ('im1', 385, 770, 300, 100, 'imp', 'arq', 'Flotado incoloro (países sin TLC)', ['124.819 t en 2025 (MinCIT)', 'China, Indonesia, Malasia', 'CIF ≈ USD 0,29/kg'],
  'La participación de países sin TLC pasó del 52 % al 87 % (2022–2025) y el precio CIF cayó de USD 0,604/kg a 0,291/kg. El proyecto de decreto reporta 61.673 t y el comunicado final 124.818,8 t: diferencia por confirmar. En 2025: China 57,7 %, Indonesia 23,7 %, Malasia 17,1 %.', ['mincit', 'mincitpd'], None),
 ('im2', 385, 885, 300, 100, 'imp', 'arq', 'Vidrio procesado listo para instalar', ['importaciones chinas +58 % en 5 años', 'precios 33–40 % menores (Acolvise)'],
  'Según Acolvise, ya no solo entra materia prima sino vidrio templado o laminado listo para instalar, que compite directamente con los transformadores nacionales. Los ingresos de la industria nacional cayeron 19 % en 2024.', ['semana25'], None),
 ('im3', 385, 1000, 300, 110, 'imp', 'aut', 'Vidrio automotriz de reposición', ['Fuyao, Xinyi (partida 7007.21)', 'no existe fabricación local de', 'parabrisas OEM identificada'],
  'La reposición automotriz se abastece con importaciones; hay registros aduaneros de parabrisas Fuyao para Renault Duster y Sandero y de vidrio Xinyi (partida 7007.21).', ['veritrade'], None),
 ('tg', 760, 325, 330, 140, 'sec', 'arq', 'Tecnoglass (Barranquilla)', ['integrada: low-e, templado, laminado,', 'IGU, ventanas y fachadas', 'USD 983,6 M (2025); 9.601 empleados', '≈96 % de ventas en EE. UU.'],
  'Transformador integrado listado en NYSE (TGLS). Complejo de 6,1 M pies², coater low-e propio, 11 hornos de templado, 9 laminadoras; ~USD 230 M invertidos en automatización desde 2023. Producto insignia: ventana de impacto ES-5000 (NOA 23-0717.25: impacto de misil grande y pequeño; según distribuidor U ≈ 3,97 W/m²K y SHGC 0,21); EPD: 61,94 kg CO₂eq/m². I+D: USD 3,1 M (0,3 % de ventas), sin patentes encontradas. Calificación: 22/25 (mejorador integrado).', ['tg10k', 'tgres', 'es5000'], 'f2_tecnoglass.png'),
 ('vp', 760, 485, 330, 100, 'sec', 'arq', 'Vidplex Universal (Bogotá)', ['pyme procesadora desde 1989', 'ventas COP 10–20 mil M (2025)', 'línea Alto Desempeño y blindado'],
  'Pyme que procesa vidrio comprado (incluido low-e). Producto insignia: línea Alto Desempeño, low-e con reflexión < 20 % y hasta 20 % de transmisión de energía solar, laminado o IGU, certificado ANSI Z97. No publica U ni SHGC. Calificación: 9/25 (adaptador); nota: una calificación baja indica poca información pública, no necesariamente poca capacidad.', ['vidplex'], 'f3_vidplex.png'),
 ('ot', 760, 605, 330, 85, 'sec', 'arq', 'Indusvit, Templacol, Vitelco', ['y cientos de pymes de templado,', 'laminado y espejo'],
  'Base amplia de transformadores. Acolvise estima más de 300 empresas y 55.000 empleos en la cadena, y reporta que varias plantas están cerca del cierre por la competencia del vidrio importado.', ['semana25'], None),
 ('agp', 760, 770, 330, 120, 'aut', 'aut', 'AGP de Colombia (Bogotá)', ['filial grupo AGP; sede de I+D', 'laboratorio balístico propio', 'B33, i-B33, Ultra Light Glass'],
  'Filial del grupo AGP (origen peruano) en Bogotá desde 1989. Planta de más de 16.000 m² con la principal estructura de I+D del grupo y laboratorio balístico propio. Ultra Light Glass: 13 mm, VPAM 2. Patentes como US8865300B2 y US11034136B2, pero el titular es AGP America S.A. (Panamá). Calificación: 22/25 (innovador).', ['agp', 'agpul', 'pat'], 'f4_agp.png'),
 ('sg', 760, 905, 330, 100, 'aut', 'aut', 'Securitglass (Bogotá)', ['pyme B2B, 11–50 empleados', 'Steel Glass 11,8 mm (NIJ IIA)', 'reproceso en autoclave'],
  'Pyme de blindaje con certificaciones declaradas NIJ 0108.01 (IIA, IIIA, III), UNE EN 1063 (BR5, BR6) e ISO 9001:2015, sin número de certificado publicado. Steel Glass: 11,8 mm, NIJ IIA, acero en el borde; declara 40 % menos peso que un vidrio de 14 mm, pero el espesor solo explica cerca del 16 %. Ofrece reproceso de vidrio delaminado. Calificación: 11/25 (adaptador con nicho).', ['sgsteel', 'sgcert'], 'f5_securitglass.png'),
 ('bt', 760, 1020, 330, 90, 'aut', 'aut', 'Ballistic Technology y otros', ['transformadores de vidrio', 'blindado nacionales'],
  'Otros transformadores nacionales de vidrio blindado (por ejemplo, Ballistic Technology, con planta desde 1997) que abastecen a las blindadoras.', ['lr22'], None),
 ('d1', 1160, 325, 310, 100, 'dis', 'arq', 'Vidrierías, instaladores', ['de fachadas y ventanería;', 'constructoras'],
  'Canal por el que el vidrio arquitectónico llega a la obra. Aquí compiten el vidrio procesado nacional y el importado listo para instalar.', ['semana25'], None),
 ('d2', 1160, 450, 310, 110, 'dis', 'arq', 'Integradores de vidrio inteligente', ['Vittrum, AVAStoreCol: instalan', 'PDLC importado; sin fabricación', 'local de la película'],
  'Instalan vidrio o película PDLC importada. Existe capacidad local de laminado y autoclave, pero no de fabricación de películas PDLC, SPD o electrocrómicas: es el margen de innovación más cercano.', ['gmi'], None),
 ('d3', 1160, 790, 310, 120, 'dis', 'aut', 'Blindadoras autorizadas (30–45)', ['1.800–2.000 vehículos/año', 'ingresos > COP 277 mil M', '(Supervigilancia, datos 2019)'],
  'Entre 30 y 45 empresas autorizadas según el año; 38.000–40.000 vehículos registrados con nivel III o superior (2022). La cifra de ingresos proviene de datos de 2019 aunque se publicó en 2026.', ['semanabl', 'lr22'], None),
 ('d4', 1160, 960, 310, 100, 'dis', 'aut', 'Talleres de reposición', ['cambio de parabrisas y', 'recalibración ADAS'],
  'El cambio de parabrisas con cámaras y sensores exige recalibrar los sistemas ADAS, lo cual agrega valor de servicio aunque el vidrio sea importado.', ['veritrade'], None),
 ('c1', 1535, 325, 315, 110, 'dem', 'arq', 'Construcción', ['≈85 % de la producción del', 'sector depende de proyectos', 'arquitectónicos (Acolvise)'],
  'Principal destino del vidrio plano. Como la NSR-10 no exige desempeño energético, la demanda local no premia los productos de mayor valor (low-e, IGU).', ['acolvisec'], None),
 ('c3', 1535, 520, 315, 100, 'dem', 'all', 'Exportación', ['EE. UU. (Florida), Región Andina,', 'Centroamérica'],
  'Tecnoglass vende cerca del 96 % a EE. UU. (más del 90 % de eso en Florida). Vidrio Andino exporta a Ecuador. AGP exporta a nivel de grupo; el porcentaje desde Colombia no es público.', ['tg10k', 'sgva'], None),
 ('c2', 1535, 700, 315, 100, 'dem', 'aut', 'Ensambladoras', ['Renault-Sofasa (34.549 u. en 2025)', 'e Hino; ≈14 % de ventas es local'],
  'Tras el cierre de GM Colmotores (2024) solo ensamblan Renault-Sofasa e Hino. Sofasa produjo 34.549 unidades en 2025 y exportó el 44 %. No se encontró información pública sobre si compra vidrio fabricado en Colombia.', ['sofasa'], None),
 ('c4', 1535, 900, 315, 100, 'dem', 'aut', 'Parque automotor', ['particulares, flotas,', 'gobierno y seguridad'],
  'Demanda de blindaje (niveles III y IV los más pedidos) y de reposición de vidrio.', ['lr22'], None),
 ('r1', 385, 1200, 300, 80, 'rec', 'none', 'Recicladores de oficio', ['≈80 % del calcín que recibe Peldar'],
  'Recogen la mayor parte del vidrio reciclado de envases. El eslabón es frágil: depende de que exista un comprador cercano.', ['peldar', 'blu'], None),
 ('r2', 1160, 1200, 310, 80, 'rec', 'arq', '«Reciclo con Vidrio Andino»', ['calcín de vidrio plano al horno'],
  'Programa que devuelve calcín de vidrio plano al horno de flotado. Más calcín significa menos energía y menos CO₂: el referente del grupo (horno Volta) opera con 88 %.', ['va'], None),
]


# ======================= NUEVA DISPOSICIÓN EN REJILLA + RUTEO ORTOGONAL =======================
BH = 110                      # alto de recuadro
ROW = [330, 490, 650, 810, 970, 1130, 1290, 1500]   # filas (R7 = reciclaje)
COLX = [60, 520, 1000, 1500, 1990]                 # x de cada columna
COLW = [280, 300, 330, 310, 315]
GAPS = [(COLX[i] + COLW[i], COLX[i + 1]) for i in range(4)]
GAPS = [(0, COLX[0])] + GAPS + [(COLX[4] + COLW[4], COLX[4] + COLW[4] + 150)]   # gap k está a la izquierda de la columna k
POS = {  # id: (columna, fila)
 'mp1': (0, 0), 'mp2': (0, 1), 'mp4': (0, 2), 'mp3': (0, 4),
 'va': (1, 0), 'gal': (1, 1), 'oi': (1, 2), 'im1': (1, 4), 'im2': (1, 5), 'im3': (1, 6), 'r1': (1, 7),
 'tg': (2, 0), 'vp': (2, 1), 'ot': (2, 2), 'agp': (2, 4), 'sg': (2, 5), 'bt': (2, 6),
 'd1': (3, 0), 'd2': (3, 1), 'd3': (3, 4), 'd4': (3, 6), 'r2': (3, 7),
 'c1': (4, 0), 'c3': (4, 1), 'c2': (4, 3), 'c4': (4, 5),
}
TOTAL_W = COLX[4] + COLW[4] + 160
GX = [40 + i * (TOTAL_W - 80) / 6 for i in range(6)]
GW = (TOTAL_W - 80) / 6 - 14
GRE = {'g1': 0, 'g2': 1, 'g3': 2, 'g4': 3, 'g5': 4, 'g6': 5}

E = [  # de, a, tipo, color, etiqueta, lado salida, lado entrada
 ('mp1', 'va', 'm', '#555', '', 'r', 'l'), ('mp2', 'va', 'm', '#555', '', 'r', 'l'), ('mp1', 'oi', 'm', '#555', '', 'r', 'l'),
 ('mp4', 'tg', 'm', '#2F4B7C', '', 'r', 'l'), ('mp3', 'tg', 'm', '#2F4B7C', '', 'r', 'l'), ('mp3', 'agp', 'm', '#8E3B2F', '', 'r', 'l'), ('mp3', 'sg', 'm', '#8E3B2F', '', 'r', 'l'),
 ('va', 'tg', 'm', '#555', 'flotado 3–10 mm', 'r', 'l'), ('va', 'vp', 'm', '#555', '', 'r', 'l'), ('va', 'ot', 'm', '#555', '', 'r', 'l'),
 ('va', 'agp', 'r', '#555', '', 'r', 'l'), ('va', 'gal', 'r', '#555', '', 'b', 't'),
 ('im1', 'vp', 'm', '#B23B2E', '', 'r', 'l'), ('im1', 'ot', 'm', '#B23B2E', '', 'r', 'l'), ('im3', 'd4', 'm', '#B23B2E', '', 'r', 'l'),
 ('tg', 'c3', 'm', '#2E7D32', '≈96 % EE. UU.', 'r', 'l'), ('tg', 'd1', 'm', '#555', '', 'r', 'l'), ('vp', 'd1', 'm', '#555', '', 'r', 'l'), ('ot', 'd1', 'm', '#555', '', 'r', 'l'),
 ('vp', 'c3', 'r', '#555', '', 'r', 'l'), ('d1', 'c1', 'm', '#2E7D32', '', 'r', 'l'), ('d2', 'c1', 'm', '#2E7D32', '', 'r', 'l'), ('mp3', 'd2', 'r', '#555', '', 'r', 'l'),
 ('agp', 'd3', 'm', '#555', '', 'r', 'l'), ('sg', 'd3', 'm', '#555', '', 'r', 'l'), ('bt', 'd3', 'm', '#555', '', 'r', 'l'), ('agp', 'c3', 'r', '#555', 'exportación del grupo', 'r', 'l'),
 ('d3', 'c4', 'm', '#2E7D32', '', 'r', 'l'), ('d4', 'c4', 'm', '#2E7D32', '', 'r', 'l'), ('c2', 'agp', 'r', '#777', '¿compra vidrio local?', 'l', 'r'),
 ('c1', 'r2', 'r', '#5B8C5A', 'residuos de obra', 'r', 'r'), ('r2', 'va', 'm', '#5B8C5A', 'calcín', 'l', 'r'), ('r1', 'oi', 'm', '#5B8C5A', '', 'r', 'r'),
]

# --- aplicar geometría
N2 = []
for row in N:
    i = row[0]; row = list(row)
    if i in GRE:
        row[1], row[2], row[3], row[4] = round(GX[GRE[i]]), 120, round(GW), BH
    else:
        c, r = POS[i]; row[1], row[2], row[3], row[4] = COLX[c], ROW[r], COLW[c], BH
    N2.append(tuple(row))
N = N2
BOX = {r[0]: dict(x=r[1], y=r[2], w=r[3], h=r[4]) for r in N}
col = {k: v[0] for k, v in POS.items()}
rowi = {k: v[1] for k, v in POS.items()}

# --- puertos: repartir las flechas a lo largo de cada lado
from collections import defaultdict
side_edges = defaultdict(list)
for idx, e in enumerate(E):
    a, b, so, si = e[0], e[1], e[5], e[6]
    side_edges[(a, so)].append((idx, b)); side_edges[(b, si)].append((idx, a))
port = {}
for (k, s), lst in side_edges.items():
    bx = BOX[k]
    lst.sort(key=lambda t: (BOX[t[1]]['y'], BOX[t[1]]['x']) if s in 'lr' else BOX[t[1]]['x'])
    n = len(lst)
    for j, (idx, other) in enumerate(lst):
        if s in 'lr':
            y = bx['y'] + bx['h'] * (j + 1) / (n + 1) + (-7 if s == 'r' else 7)
            x = bx['x'] + (bx['w'] if s == 'r' else 0)
        else:
            x = bx['x'] + bx['w'] * (j + 1) / (n + 1)
            y = bx['y'] + (bx['h'] if s == 'b' else 0)
        port[(idx, k, s)] = (round(x), round(y))

# --- carriles verticales (en los huecos entre columnas) y corredores horizontales (entre filas)
def gap_of(k, s):
    return col[k] + 1 if s == 'r' else col[k]
lanes = defaultdict(list)       # gap -> [idx,...]
corr = defaultdict(list)        # banda -> [idx,...]
plan = {}
for idx, e in enumerate(E):
    a, b, so, si = e[0], e[1], e[5], e[6]
    if so in 'tb':
        plan[idx] = ('direct',); continue
    ga, gb = gap_of(a, so), gap_of(b, si)
    pa, pb = port[(idx, a, so)], port[(idx, b, si)]
    if ga == gb:
        plan[idx] = ('one', ga); lanes[ga].append(idx)
    else:
        rb = rowi[b]
        band = rb if pa[1] > pb[1] else rb - 1     # hueco justo debajo o encima de la fila destino
        band = min(max(band, 0), 6)
        plan[idx] = ('two', ga, gb, band); lanes[ga].append(idx); lanes[gb].append(idx); corr[band].append(idx)

lane_x = {}
for g, lst in lanes.items():
    x0, x1 = GAPS[g]
    if g == 0: x0 = x1 - 40
    if g == 5: x1 = x0 + 120
    n = len(lst); step = min(18, (x1 - x0 - 40) / max(1, n - 1)) if n > 1 else 0
    start = (x0 + x1) / 2 - step * (n - 1) / 2
    # orden: las que salen hacia arriba a un lado, hacia abajo al otro, para reducir cruces
    lst.sort(key=lambda i: port[(i, E[i][0], E[i][5])][1] - port[(i, E[i][1], E[i][6])][1])
    for j, i in enumerate(lst):
        lane_x[(i, g)] = round(start + j * step)
corr_y = {}
for band, lst in corr.items():
    y0 = ROW[band] + BH; y1 = ROW[band + 1]
    n = len(lst); step = min(9, (y1 - y0 - 16) / max(1, n - 1)) if n > 1 else 0
    start = (y0 + y1) / 2 - step * (n - 1) / 2
    lst.sort(key=lambda i: BOX[E[i][1]]['x'])
    for j, i in enumerate(lst):
        corr_y[(i, band)] = round(start + j * step)

edges = []
for idx, e in enumerate(E):
    a, b, k, c, l, so, si = e
    p = plan[idx]
    if p[0] == 'direct':
        pa = (BOX[a]['x'] + BOX[a]['w'] // 2, BOX[a]['y'] + BOX[a]['h'])
        pb = (pa[0], BOX[b]['y'])
        pts = [pa, pb]; lp = (pa[0] + 8, (pa[1] + pb[1]) / 2)
    else:
        pa, pb = port[(idx, a, so)], port[(idx, b, si)]
        if p[0] == 'one':
            x = lane_x[(idx, p[1])]
            pts = [pa, (x, pa[1]), (x, pb[1]), pb]
        else:
            xa, xb, y = lane_x[(idx, p[1])], lane_x[(idx, p[2])], corr_y[(idx, p[3])]
            pts = [pa, (xa, pa[1]), (xa, y), (xb, y), (xb, pb[1]), pb]
        # etiqueta sobre el tramo horizontal más largo
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1) if pts[i][1] == pts[i + 1][1]]
        s0 = max(segs, key=lambda s: abs(s[1][0] - s[0][0]))
        lp = ((s0[0][0] + s0[1][0]) / 2, s0[0][1] - 6)
    # quitar puntos redundantes
    clean = [pts[0]]
    for q in pts[1:]:
        if q != clean[-1]: clean.append(q)
    edges.append(dict(a=a, b=b, k=k, c=c, l=l, p=clean, lp=lp))

def frame(c0, c1, r0, r1, label, color, pad=18):
    x0 = COLX[c0] - pad; x1 = COLX[c1] + COLW[c1] + pad
    return (x0, ROW[r0] - 40, x1 - x0, ROW[r1] + BH + pad - (ROW[r0] - 40), label, color)
GROUPS = [
 (20, 80, TOTAL_W - 40, 160, 'GREMIOS E INSTITUCIONES', '#A66A00'),
 frame(1, 1, 0, 2, 'Vidrio plano y envases', '#1F3A68'), frame(1, 1, 4, 6, 'Importaciones', '#B23B2E'),
 frame(2, 2, 0, 2, '3a. Arquitectónica: >300 empresas', '#2F4B7C'), frame(2, 2, 4, 6, '3b. Automotriz (blindaje)', '#8E3B2F'),
 (20, ROW[7] - 45, TOTAL_W - 40, BH + 75, '6. RECICLAJE Y CIERRE DE CICLO', '#5B8C5A'),
]
COLS = [(COLX[i] + COLW[i] / 2, t) for i, t in enumerate(['1. MATERIAS PRIMAS E INSUMOS', '2. TRANSFORMACIÓN PRIMARIA', '3. TRANSFORMACIÓN SECUNDARIA', '4. DISTRIBUCIÓN Y SERVICIOS', '5. DEMANDA'])]
H_TOTAL = ROW[7] + BH + 70

def img64(f):
    im = Image.open(f).convert('RGB')
    im.thumbnail((760, 1000))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

nodes = []
for (i, x, y, w, h, t, sec, ti, ls, det, src, dg) in N:
    nodes.append(dict(id=i, x=x, y=y, w=w, h=h, t=t, sec=sec, ti=ti, ls=ls, det=det,
                      src=[{'l': U[s][0], 'u': U[s][1]} for s in src], img=img64(dg) if dg else None))
data = dict(nodes=nodes, edges=edges, groups=GROUPS, cols=COLS, W=TOTAL_W, H=H_TOTAL, colY=ROW[0] - 52)
html = open('mapa_template.html').read().replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
open('mapa_ecosistemico_interactivo.html', 'w').write(html)
print('ok', len(html) // 1024, 'KB', 'W', TOTAL_W, 'H', H_TOTAL)
