## 1. Introduce

제안된 방법은 다음과 같은 것을 포함한다.
1. morphological method, zone projection을 통한 text-line 분리.
2. 각각의 text line에 대해 vertical projection, Stroke Width Transform(SWT), bridge finding, Voronoi Diagram을 이용한 글자 분리.

ICDAR segmentation contest 2013에 의하면 INMC가 가장 인식률이 높다. 
(INMC는 저번 중국어 논문과 같은 방식)
이 방법은 ICDAR의 텍스트 페이지에 대해 98%가 넘는 인식률을 자랑하지만 복잡하고 각 text line의 휜 정도나 텍스트라인 사이의 distance를 학습하는데에 시간이 든다.
그래서 우리는 closing morphology를 통해 text page를 smearing하고 zone projection profile을 통해 text-line을 분리한다. 
 
여러 segmentation에 대한 설명 주저리주저리..
Coarse Segmentatio은 vertical projection과 SWT를 사용한다. SWT는 일반적인 이미지에서 텍스트를 찾기 위해 개발되었다. 근데 이게 coarse segmentation에서는 지대한 영향을 줌. 
Fine Segmentation에서는 bridge finding과 Voronoi diagram을 이용한다. 
우리는 가장 단순한 접근을 선택했는데 좋은 결과를 낸다

Section 2에서는 textline segmentation에 대해 기술하고, section 3에서는 character segmentation 방법을 제공한다. section4는 결과, section5는 결론.

## 2. Text-line Segmentation

보통 사람은 글을 line이 없는 페이퍼에서는 똑바로 쓰지 않는 경향이 있기 때문에, global projection에 기초를 둔 text line segmentation은 불안정하다. 

먼저 SIS(simple image Statics)를 이용해 스캔된 document를 이진화시킨다. 이건 Otus에 의한 가장 유명한 binarization 알고리즘보다 빠르다. 그다음으로는 text line 사이의 접촉을 완화시키기 위해 세선화를 진행한다. text line 사이와 빈 공간을 강조하기 위해서 우리는 closing morphology(erode 후에  dilate하는 것)를 사용한다. 
   
여기서 elem은 column이 row보다 많은 행렬(가로로 긴 사각형)을 의마한다. 우리의 시스템에서 17 columns에 3rows를 선택했다. 결과는 figure 3에 나타나 있는데, 거기서 text line의 지역이 강조되고 touching regions(맞물려있는 곳)은 거의 영향을 받지 않는다. 

![Fig3](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Fig3.png)

그 다음으로 우리는 text page를 n개의 줄로 나눴는데 이 줄의 두께는 글자의 밀도와 관련이 있다. width  of stripe  은 아래와 같다.
![Func1](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func1.PNG)

W,H는 documnent image I 의 width 와 heigh이고, I(x,y)는 (x,y)의 픽셀값.
(그니까 저 if 문이 밀도 구하는 공식.)
밀도에 따라 각각의 s_i에 대해 같은 width를 가지면서 줄의 수는 4부터 20까지 바뀐다 horizontal projection profile  은 각 strip에 대해 계산되고, 길이 7짜리 window의 평균필터를 이동하는 것으로 완화된다.:

![Func2](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func2.PNG)

각각의 stripes에서 projection profile에 smoothing을 실행하고 난 결과는 Figure4에 나타나며 잘못된 피크나 협곡(낮아지는 부분)이 제거된다. 

![Figure4](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Fig4.png)

이것은 분리할 곳을 threshold를 통해 더 효과적으로 정해준다. 각 strip의 Threshold 는 아래와 같이 계산된다. 

![Func3](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func3.PNG)

알파는 상수이고, 우리 시스템에서는 10으로 잡았다. 
각 stripes안에서 위와 아래 경계 (valley)는 아래와 같이 결정된다. 

![Func4](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func4.PNG)

경계는 경계사이의 distance가 평균 distance D 보다 작을 경우 합쳐진다. 

![Func5](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func5.PNG)

이때 N은 위경계와 아랫경계의 짝의 수. 
 끝으로 우리는 i의 AB와 BB를 인접한 stripe i+1의 것과 합쳐 text line을 얻는다. 

## 3. Character Segmentation

먼저 [SWT알고리즘](http://iskim3068.tistory.com/100)을 이용하여 텍스트 패이지 내의 모든 획의 평균  너비를 구한다. SWT의 원래 목적은 자연적인 사진에서 많은 폰트와 언어의 글자를 찾는데에 있다. 하지만 우리는 SWT를 coarse segmentation을 위해 사용할거야. SWT는 Canny edge detection을 이용해서 각각의 이미지픽셀에 대해 획의 넓이가 유사하게 만들어진 행렬을 산출한다. 그러므로 평균 획 넓이(AW) 는 아래와 같이 계산된다.

![Func6](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Func6.PNG)

I'(x,y)는 SWT이후의 픽셀값이고, I(x,y)는 이전의 binary image 픽셀값 (둘다 바이너리인가보다.)
두 번째로, 우리는 closing morphology를 여기서는 3by 15 인 가로로 긴 매트릭스 이용) 각각의 텍스트라인에 적용해준다. 세 번째로 우리는 vertical projection profile  를   각각의 텍스트 라인 j에 대해 적용한다. 그리고 텍스트라인을 value 가 0인 지점에 따라 나눈다. 그 후 우리는 텍스트 라인 내의 각 나눠진 구역의 평균 넓이를 구한다. 네 번째로 우리는 크기가 평균에 비해 큰 것들에 대해 projection값이 AW보다 낮은 게 있으면 그 지점에 따라 자른다. 잘못된 segmentation을 방지하기 위해, segmentation이 매우 작은 component를 생성하는 경우 대형 segment 내의 projection profile의 최고값 사이의 범위에서 투영 값을 고려한다. 이 대충한 segmentation은 접촉해있지 않은 글자와 선 하나만 접촉한 글자를 효과적으로 분할한다. SWT없이는 우리는 AW의 threshold값을 설정하기 위한 공통 획 넓이를 구할 수 없다. AW를 이용한 projection profile에 의한 분할은 아래 나와 있다.

![Fig5](https://github.com/lkiung/Hangul-Doc_analysis/blob/master/Figure/Fig5.png)

이 예시에서는 zero point segmentation (projection 시킨 값이 0)이 먼저 segment 4와 5사이에 실행된다. segment(1,2,3)은 oversized 되었기 때문에, AW threshold를 통해 1,2,3으로 분할된다. segmentation 3은 분할되면 2개의 매우 작은 component로 분할되기 때문에 더 이상 분할되지 않는다.
