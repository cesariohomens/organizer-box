# Caixa organizadora com paredes em favo de mel

Recriação paramétrica em OpenSCAD da caixa `200x100_4_V2.stl`, com as mesmas
medidas exteriores mas com as nervuras do favo 1/3 mais finas (2 mm → 1,333 mm).

| | Original | Esta caixa |
|---|---|---|
| Exterior | 100 × 200 × 64 mm | igual |
| Parede | 3 mm | igual |
| Fundo | 2 mm (3 mm junto à parede) | igual |
| Aro maciço no topo | 8 mm | igual |
| Passo da célula hexagonal | 10 mm entre faces | igual |
| **Nervura entre células** | **2 mm** | **1,333 mm** |
| **Furo hexagonal** | **8 mm entre faces** | **8,667 mm** |

A malha hexagonal ocupa exactamente as mesmas posições do original: só a
espessura do material entre furos mudou, por isso as duas caixas encaixam lado
a lado com o mesmo aspecto.

## Ficheiros

- `index.html` — gerador no browser, para caixas de qualquer medida
- `organizer_box.scad` — modelo paramétrico
- `organizer_box_100x200x64_rib1.33.stl` — STL pronto a imprimir
- `tools/` — utilitários de engenharia inversa e verificação do STL original

## Gerador no browser

Abre `index.html` (basta fazer duplo clique, não precisa de servidor). Escolhes
as medidas exteriores, a parede, o fundo, os dois aros maciços e o raio dos
cantos, vês a peça em 3D e descarregas o STL ou o `.scad` correspondente.

O favo vive entre os dois aros. O de cima dá rigidez à boca; o de baixo fecha a
parede junto ao fundo, para os conteúdos pequenos não escaparem pela primeira
fiada de furos. A caixa original não tem aro inferior, por isso `base_h = 0` no
`organizer_box.scad`; a app começa em 8 mm, simétrico ao de cima.

A célula e a nervura do favo não acompanham o tamanho da caixa: uma caixa maior
leva mais favos, todos do mesmo tamanho, para que peças diferentes fiquem com o
mesmo aspecto lado a lado.

A malha sai fechada e manifold, verificada por varrimento em milhares de
combinações de medidas.

Nos troços rectos da parede a app e o OpenSCAD dão a mesma peça, até à precisão
da facetagem dos cantos (centésimas de milímetro). Dentro dos arcos dos cantos
divergem por construção: o OpenSCAD abre os furos como prismas a direito, que
atravessam a curva de esguelha e lhe arrancam uma lasca, enquanto a app os
enrola ao longo do perímetro, de modo a ficarem sempre normais à parede. Nas
caixas em que a coluna mais exterior chega bem dentro do canto, a diferença vai
a 2 mm nessa zona. A versão da app é a mais sã das duas — deixa o canto inteiro
—, e é também o que permite manter o mesmo favo em qualquer tamanho de caixa.

O `.scad` exportado é o `organizer_box.scad` deste repositório com o bloco de
parâmetros reescrito. `make embed` volta a copiá-lo para dentro da página
sempre que o modelo mudar.

## Gerar

```bash
make            # exporta o STL
make preview    # imagem PNG em build/
```

Requer OpenSCAD (testado com 2021.01). A renderização demora cerca de 20 s.

## Parâmetros

Todos no topo de `organizer_box.scad`. Os mais úteis:

```openscad
cell   = 10;    // passo da célula, entre faces
rib    = 4 / 3; // material entre células (2 no original)
base_h = 0;     // aro maciço em baixo (0 = como o original)
rim_h  = 8;     // aro maciço em cima
```

Para outra espessura de nervura basta sobrepor na linha de comandos:

```bash
openscad -o saida.stl --export-format binstl -D rib=1 organizer_box.scad
```

## Verificação

O modelo foi validado contra o STL original: com `rib = 2` reproduz a peça de
origem. `make validate` lança 6819 raios através das duas malhas e compara os
intervalos de material — nenhum desvio acima de 0,06 mm.

```bash
pip install -r requirements.txt
make validate   # compara com o original (REF=... para outro caminho)
make verify     # mede a caixa final (bbox, nervuras, furos, parede)
```

## Impressão

Sem suportes, com o fundo na mesa. As nervuras de 1,333 mm saem com 3 a 4
perímetros num bico de 0,4 mm; se o teu fatiador as deixar ocas, reduz a largura
de extrusão ou aumenta `rib`.
