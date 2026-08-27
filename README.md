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
mais favos, todos do mesmo tamanho.

## Opções

- **Fundo em colmeia** — fura o fundo com a mesma grelha hexagonal
- **Pegas nas paredes** — abre um furo hexagonal largo perto do topo em cada
  parede que escolheres (+X, −X, +Y, −Y)
- **Tampa** — peça sólida com uma saia inferior que encaixa na boca da caixa,
  com profundidade e folga reguláveis. Podes combinar à vontade furação para
  pega e malha em colmeia, ou deixar a tampa lisa. A pré-visualização 3D
  permite ver a caixa, a tampa ou as duas, e descarregar STLs separados

## Uso

1. Abre `index.html` no browser
2. Ajusta medidas, grelha, pegas e tampa
3. Vê a peça em 3D e descarrega o STL

A interface está em inglês, português, espanhol, francês, alemão, italiano,
chinês simplificado e japonês.

## Impressão

Sem suportes, com o fundo na mesa. As nervuras de 1,333 mm saem com 3 a 4
perímetros num bico de 0,4 mm; se o teu fatiador as deixar ocas, reduz a largura
de extrusão ou aumenta a nervura na app.
