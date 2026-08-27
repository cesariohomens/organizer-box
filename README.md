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
- **Pegas nas paredes** — abre uma ranhura oval perto do topo em cada parede que
  escolheres (+X, −X, +Y, −Y), com a mesma forma da pega da tampa
- **Porta-etiquetas** — moldura saliente no topo de cada parede que escolheres,
  assente na superfície exterior. Só tem borda inferior e laterais: a etiqueta
  entra por cima e fica à vista, presa pela soleira e pelos retornos das duas
  calhas — os três encaixes agarram 2,5 mm cada, para a moldura fechar por
  igual. A bolsa tem 2,4 mm, para uma etiqueta impressa de 2 mm. A soleira
  leva um chanfre a 45° por baixo, por isso imprime sem suportes. Os dois
  cantos de baixo da abertura são arredondados — a soleira sobe para as calhas
  em arco — e o cartão faz a mesma curva; em cima ficam a direito, que é por
  onde a etiqueta entra e se puxa. A mesma parede pode levar pega e
  porta-etiquetas: nesse caso a moldura desce para debaixo da pega. Se a caixa
  for baixa de mais para as duas coisas, a app diz quais as paredes onde não
  cabem
- **Etiquetas escritas** — cada porta-etiquetas ligado abre um campo de texto.
  O que escreveres vira uma placa à parte: 2 mm de base e 1 mm de letra em
  relevo, na Exo, com o corpo a crescer até encher a janela da moldura. A placa
  aparece no sítio na pré-visualização e sai num STL próprio, já deitada com o
  texto para cima, que é como tem de ser impressa. Se a caixa for pequena para
  o texto que escreveste, a app avisa antes de as letras ficarem mais finas do
  que um cordão de material
- **Largura da etiqueta** — por baixo do texto podes dar a cada parede a
  largura que quiseres, em milímetros. A moldura acompanha a etiqueta, para
  esta não abanar lá dentro, e o campo diz sempre o tamanho que vai sair. Deixa
  o campo vazio e a etiqueta volta a ocupar a parede toda; pedir mais do que a
  parede aguenta ou menos do que a moldura fecha fica pelo limite
- **Cores da etiqueta** — a base começa 20% mais escura do que a caixa e a
  letra fica preta ou branca, conforme a que se destaca da base: uma caixa
  branca dá letra preta e uma caixa preta dá letra branca. Os dois seletores
  deixam-te escolher outra coisa, e aí a cor fica onde a puseste. Só conta para
  a pré-visualização — o STL não leva cor
- **Tampa** — peça sólida que usa o mesmo encaixe das caixas: por baixo leva o
  pé chanfrado da caixa, por cima leva o rebaixo da boca. Assenta na caixa como
  uma caixa empilhada e ainda podes empilhar outra caixa por cima da tampa
  fechada. A folga afina o aperto do pé conforme a impressora. Podes combinar à
  vontade furação para pega e malha em colmeia, ou deixar a tampa lisa. A
  pré-visualização 3D permite ver a caixa, a tampa ou as duas, e descarregar
  STLs separados

## Uso

1. Abre `index.html` no browser
2. Ajusta medidas, grelha, pegas, porta-etiquetas e tampa
3. Escreve o texto das etiquetas que quiseres, e dá-lhes largura e cor
4. Vê as peças em 3D e descarrega os STL

A interface está em inglês, português, espanhol, francês, alemão, italiano,
chinês simplificado e japonês.

## Impressão

Sem suportes, com o fundo na mesa. As nervuras de 1,333 mm saem com 3 a 4
perímetros num bico de 0,4 mm; se o teu fatiador as deixar ocas, reduz a largura
de extrusão ou aumenta a nervura na app.

As etiquetas imprimem-se deitadas, sem suportes. O texto começa na camada dos
2 mm, por isso é aí que podes trocar de filamento se quiseres a letra noutra
cor.
