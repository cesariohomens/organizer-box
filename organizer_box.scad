// Caixa organizadora com paredes em favo de mel.
//
// Reproduz a geometria de 200x100_4_V2.stl (100 x 200 x 64 mm, cantos em
// superelipse, aro macico no topo) com a espessura da nervura do favo
// configuravel. O original usa rib = 2; este ficheiro usa 4/3 (1/3 mais fino).
//
// base_h acrescenta um aro macico tambem em baixo, que o original nao tem; os
// valores por omissao ficam fieis a peca de origem.

/* [Corpo] */
box_x = 100;         // largura
box_y = 200;         // comprimento
box_z = 64;          // altura
corner_r = 10;       // raio dos cantos
corner_n = 2.4;      // expoente da superelipse dos cantos
wall = 3;            // espessura da parede
floor_t = 2;         // espessura do fundo ao centro
floor_chamfer = 1;   // chanfro a 45 graus na juncao fundo/parede
base_chamfer = 2.5;  // chanfro a 45 graus na aresta inferior exterior
base_h = 0;          // banda macica acima do fundo (o original nao tem)
rim_h = 8;           // banda macica sob o bordo superior
rim_chamfer = 2.5;   // chanfro a 45 graus no bordo interior de topo

/* [Favo de mel] */
cell = 10;           // passo da celula, medido entre faces
rib = 4 / 3;         // material entre celulas vizinhas (original: 2)
row_z0 = undef;      // cota de uma fiada; undef = escolhida automaticamente
row_keep = 0.3;      // fraccao minima de um furo cortado pelo fundo ou pelo aro

/* [Qualidade] */
corner_steps = 60;   // segmentos por canto da superelipse
$fs = 0.4;
$fa = 2;

SQRT3 = 1.7320508075688772;

hole_r = (cell - rib) / SQRT3;   // circunraio do furo hexagonal
col_pitch = cell / SQRT3 * 1.5;  // distancia horizontal entre colunas
row_pitch = cell;                // distancia vertical dentro da mesma coluna

floor_top = floor_t + floor_chamfer;  // cota do fundo junto a parede

// A banda perfurada vive entre os dois aros macicos.
band_bottom = floor_top + base_h;
rim_bottom = box_z - rim_h;

eps = 0.01;

// ---------------------------------------------------------------- perfil 2D

// Um quadrante de superelipse: |u|^n + |v|^n = 1.
function se_arc(cx, cy, sx, sy, r, n, rev) =
    [for (i = [0:corner_steps])
        let (t = rev ? 90 - i * 90 / corner_steps : i * 90 / corner_steps)
        [cx + sx * r * pow(cos(t), 2 / n), cy + sy * r * pow(sin(t), 2 / n)]];

// Rectangulo w x l centrado na origem com cantos em superelipse de raio r.
function squircle_rect(w, l, r, n) =
    let (cx = w / 2 - r, cy = l / 2 - r)
    concat(
        se_arc( cx,  cy,  1,  1, r, n, false),
        se_arc(-cx,  cy, -1,  1, r, n, true),
        se_arc(-cx, -cy, -1, -1, r, n, false),
        se_arc( cx, -cy,  1, -1, r, n, true));

module outline(w, l) {
    polygon(squircle_rect(w, l, corner_r, corner_n));
}

function path_len(p, i = 0) = i + 1 < len(p) ? norm(p[i + 1] - p[i]) + path_len(p, i + 1) : 0;

corner_len = path_len(se_arc(0, 0, 1, 1, corner_r, corner_n, false));

// Tronco recto entre dois perfis 2D, usado para os chanfros a 45 graus.
module taper(z0, z1) {
    hull() {
        translate([0, 0, z0]) linear_extrude(eps) children(0);
        translate([0, 0, z1 - eps]) linear_extrude(eps) children(1);
    }
}

// ------------------------------------------------------------------- solido

module shell() {
    translate([0, 0, base_chamfer])
        linear_extrude(box_z - base_chamfer) outline(box_x, box_y);
    taper(0, base_chamfer) {
        offset(r = -base_chamfer) outline(box_x, box_y);
        outline(box_x, box_y);
    }
}

module cavity() {
    iw = box_x - 2 * wall;
    il = box_y - 2 * wall;

    taper(floor_t, floor_top) {
        offset(r = -floor_chamfer) outline(iw, il);
        outline(iw, il);
    }
    translate([0, 0, floor_top - eps])
        linear_extrude(box_z - rim_chamfer - floor_top + eps) outline(iw, il);
    taper(box_z - rim_chamfer, box_z + eps) {
        outline(iw, il);
        offset(r = rim_chamfer) outline(iw, il);
    }
}

// --------------------------------------------------------------- favo de mel

hole_hh = (cell - rib) / 2;              // meia altura do furo, entre faces
slot_pitch = row_pitch / 2;              // fiadas pares e impares intercalam
band_mid = (band_bottom + rim_bottom) / 2;

function slot_m0(z0) = floor((band_bottom - hole_hh - z0) / slot_pitch);
function slot_m1(z0) = ceil((rim_bottom + hole_hh - z0) / slot_pitch);

// Quanto resta de um furo depois de cortado pelos dois aros, em fraccao da sua
// altura. Zero quando a fiada nao chega a banda perfurada.
function slot_kept(zc) =
    max(0, min(zc + hole_hh, rim_bottom) - max(zc - hole_hh, band_bottom)) / (2 * hole_hh);

function sum(v, i = 0) = i < len(v) ? v[i] + sum(v, i + 1) : 0;

// Area aberta que uma dada fase deixa, ignorando os furos demasiado cortados.
function phase_open(z0) =
    sum([for (m = [slot_m0(z0):slot_m1(z0)])
            let (k = slot_kept(z0 + m * slot_pitch)) k >= row_keep ? k : 0]);

// Duas fases mantem a malha simetrica na banda: uma fiada ao centro, ou duas a
// ladea-lo. Fica a que deixa mais furo aberto.
function auto_z0() =
    phase_open(band_mid + slot_pitch / 2) > phase_open(band_mid)
        ? band_mid + slot_pitch / 2 : band_mid;

z0 = is_undef(row_z0) ? auto_z0() : row_z0;

// Campo de hexagonos no plano da parede: x tangencial, y = cota z real.
// So entram celulas cujo centro cai no troco recto da parede e cujo furo nao
// passa do meio do canto, onde comeca a parede seguinte.
module hex_field(half_span) {
    nj = min(floor(half_span / col_pitch),
             floor((half_span + corner_len / 2 - hole_r) / col_pitch));

    intersection() {
        union() {
            for (j = [-nj:nj], m = [slot_m0(z0):slot_m1(z0)])
                if ((j - m) % 2 == 0 && slot_kept(z0 + m * slot_pitch) >= row_keep)
                    translate([j * col_pitch, z0 + m * slot_pitch])
                        circle(r = hole_r, $fn = 6);
        }
        translate([0, band_mid])
            square([2 * half_span + 4 * hole_r, rim_bottom - band_bottom], center = true);
    }
}

module honeycomb() {
    // Paredes longas (normal em X).
    rotate([90, 0, 90])
        linear_extrude(box_x + 20, center = true) hex_field(box_y / 2 - corner_r);
    // Paredes curtas (normal em Y).
    rotate([90, 0, 0])
        linear_extrude(box_y + 20, center = true) hex_field(box_x / 2 - corner_r);
}

// --------------------------------------------------------------------- peca

difference() {
    shell();
    cavity();
    honeycomb();
}
