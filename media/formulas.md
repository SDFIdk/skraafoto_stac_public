I dette dokument skrives formler i mathjax. GitHub markdown understøtter ikke dette, så formlerne renderes til billeder, der kan sættes ind.

$$
K = \begin{bmatrix} -f & 0 & x0 \\  0 & -f & y0 \\ 0 & 0 & 1 \end{bmatrix}
$$


$$
R = \begin{bmatrix} m11 & m12 & m13 \\ m21 & m22 & m23 \\ m31 & m32 & m33 \end{bmatrix} 
$$


$$
T = \begin{bmatrix} 1 & 0 & 0 & -Xc \\  0 & 1 & 0 & -Yc \\ 0 & 0 & 1 & - Zc \end{bmatrix}
$$



$$
\begin{bmatrix}xc \\ yc \\ zc \end{bmatrix} = KRT \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}
$$


$$
(xa, ya) = (xc / zc, yc / zc)
$$