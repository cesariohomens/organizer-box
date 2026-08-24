# Caixa organizadora com paredes em favo de mel

Gerador no browser para caixas de impressão 3D com paredes em grelha hexagonal.
Abre `index.html` (basta fazer duplo clique, não precisa de servidor), escolhe as
medidas e descarrega o STL.

## Valores por omissão

| | |
|---|---|
| Exterior | 100 × 200 × 64 mm |
| Parede | 3 mm |
| Fundo | 3 mm |
| Aro inferior | 7 mm |
| Aro superior | 7 mm |
| Passo da célula | 10 mm entre faces |
| Nervura | 1,333 mm |

A célula e a nervura não acompanham o tamanho da caixa: uma caixa maior leva
mais favos, todos do mesmo tamanho, para que peças diferentes fiquem com o
mesmo aspecto lado a lado.

O favo vive entre os dois aros maciços. O de cima dá rigidez à boca; o de baixo
fecha a parede junto ao fundo. Com o aro inferior a 0 o favo começa logo acima
do fundo.

## Uso

1. Abre `index.html` no browser
2. Ajusta largura, comprimento, altura, parede, fundo, aros e raio dos cantos
3. Vê a peça em 3D e descarrega o STL binário

A malha sai fechada e manifold, verificada por varrimento em milhares de
combinações de medidas.

## Impressão

Sem suportes, com o fundo na mesa. As nervuras de 1,333 mm saem com 3 a 4
perímetros num bico de 0,4 mm; se o teu fatiador as deixar ocas, reduz a largura
de extrusão ou aumenta a nervura na app.
