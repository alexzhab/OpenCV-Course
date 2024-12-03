## ДЗ 4: 3D реконструкция

#### Описание алгоритма

1. Рассмотрим следующее изображение.

<img src="samples/left02.jpg" alt="orig"  width="400" />

2. Уберем искажение с изображения шахматной доски с помощью калибровки камеры.

<img src="after_undistort/left02.png" alt="after_undistort"  width="400" />

3. Отметим крестиками места, где впоследствии будут стоять фигуры.

<img src="with_crosses/02.png" alt="with_crosses"  width="400" />

4. С помощью `cv2.matchTemplate` найдем позиции крестиков на изображении.

<img src="found_crosses/02.jpg" alt="found_crosses"  width="400" />

5. Найдём квадранты сетки, где лежат крестики, и построим на них красные 3D конусы.

<img src="res/02.jpg" alt="res"  width="400" />

Ещё примеры:

<img src="res/08.jpg" alt="res"  width="400" />
