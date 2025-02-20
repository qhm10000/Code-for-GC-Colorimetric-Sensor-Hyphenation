1.	import cv2  
2.	import numpy as np  
3.	import copy  
4.	import pandas as pd  
5.	import sys  
6.	  
7.	points = []  
8.	cur_point = []  
9.	start_point = []  
10.	shape_color = (255, 255, 255)  
11.	window = "Preview"  
12.	draw_img = {}  
13.	selected = False  
14.	x0 = 0  
15.	y0 = 0  
16.	show_count = False  
17.	  
18.	def on_mouse(event, x, y, flags, param):  
19.	    global points, img, draw_img, cur_point, start_point, selected, show_count  
20.	    h, w = img.shape[:2]  
21.	  
22.	    mask_img = np.zeros([h + 2, w + 2], dtype=np.uint8)  
23.	  
24.	    repeat_count = 0  
25.	    if  event == cv2.EVENT_LBUTTONDOWN:  
26.	        selected = False  
27.	        if repeat_count == 0:  
28.	            draw_img = copy.deepcopy(img)  
29.	            points.clear()  
30.	        start_point = [x + x0, y + y0]  
31.	        points.append(start_point)  
32.	        repeat_count += 1  
33.	  
34.	    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  
35.	        selected = False  
36.	        cur_point = [x + x0, y + y0]  
37.	        points.append(cur_point)  
38.	  
39.	    elif event == cv2.EVENT_LBUTTONUP:  
40.	        repeat_count = 0  
41.	        cur_point = [x + x0, y + y0]  
42.	        points.append(cur_point)  
43.	        selected = True  
44.	        show_count = True  
45.	  
46.	if __name__ == "__main__":  
47.	    if len(sys.argv) != 2:  
48.	        print("Please enter the video file path!")  
49.	        exit()  
50.	  
51.	    path = sys.argv[1]  
52.	  
53.	    v = cv2.VideoCapture(path)  
54.	    frames = -1  
55.	    frame_rate = v.get(cv2.CAP_PROP_FPS)  
56.	    seconds = 0  
57.	  
58.	    cv2.namedWindow(window)  
59.	    cv2.setMouseCallback(window, on_mouse, 0)  
60.	    cv2.moveWindow(window, x0, y0)  
61.	  
62.	    rgb = {  
63.	        "R": [],  
64.	        "G": [],  
65.	        "B": [],  
66.	        "pixels": []  
67.	    }  
68.	    start = False  
69.	    img = []  
70.	    draw_img = None  
71.	    img_changed = False  
72.	    last_point = 0  
73.	    while (v.isOpened()):  
74.	        width  = cv2.getWindowImageRect(window)[2]  
75.	        height = cv2.getWindowImageRect(window)[3]  
76.	        if (start == False and len(img) == 0) or start == True:  
77.	            while True:  
78.	                ret, img = v.read()  
79.	                frames += 1  
80.	                if img is None or frames % int(frame_rate) == 0:  
81.	                    break  
82.	  
83.	            img_changed = True  
84.	            if img is None:  
85.	                start = False  
86.	                df = pd.DataFrame(rgb)  
87.	                df.to_csv(path + ".csv")  
88.	                print("Process Done! Check %s.csv" % (path))  
89.	                break  
90.	  
91.	        if (img_changed or last_point != len(points)) and len(points) > 0:  
92.	            last_point = len(points)  
93.	            img_changed = False  
94.	            draw_img = copy.deepcopy(img)  
95.	            start_point = points[0]  
96.	            cv2.circle(draw_img, tuple(start_point), 1, shape_color,0)  
97.	            length = len(points)  
98.	            i = 1  
99.	            while i < length:  
100.	                cur_point = points[i]  
101.	                cv2.line(draw_img, tuple(points[i - 1]), tuple(cur_point), shape_color)  
102.	                i += 1  
103.	            if selected:  
104.	                cv2.line(draw_img, tuple(points[-1]), tuple(points[0]), shape_color)  
105.	                cv2.circle(draw_img, tuple(points[0]), 1, shape_color, 0)  
106.	  
107.	            if (start and selected) or show_count:  
108.	                print("Start to process RGB values")  
109.	                h, w = img.shape[:2]  
110.	                mask_img = np.zeros([h + 2, w + 2], dtype=np.uint8)  
111.	                ret, image, mask, rect = cv2.floodFill(draw_img, mask_img, points[-1], shape_color, cv2.FLOODFILL_FIXED_RANGE)  
112.	                src =cv2.bitwise_and(draw_img, image)  
113.	  
114.	                gray = cv2.cvtColor(draw_img, cv2.COLOR_BGR2GRAY)  
115.	  
116.	                ret, binary = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)  
117.	  
118.	                contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
119.	  
120.	                contour = []  
121.	                if len(contours) > 0:  
122.	                    contour.append(contours[0])  
123.	                    for c in contours:  
124.	                        if c.size > contour[0].size:  
125.	                            contour[0] = c  
126.	  
127.	                cv2.drawContours(draw_img, contour, -1, (0, 0, 255), 2)  
128.	  
129.	                print("Start to process the %s second(s)" % (seconds))  
130.	                count = 0  
131.	                bgr = np.zeros((3))  
132.	                min_x = draw_img.shape[1]  
133.	                min_y = draw_img.shape[0]  
134.	                max_x = 0  
135.	                max_y = 0  
136.	  
137.	                for c in contour[0]:  
138.	                    min_x = min(c[0][0], min_x)  
139.	                    min_y = min(c[0][1], min_y)  
140.	                    max_x = max(c[0][0], max_x)  
141.	                    max_y = max(c[0][1], max_y)  
142.	  
143.	                for y in range(min_y, max_y):  
144.	                    for x in range(min_x, max_x):  
145.	                        position = (x, y)  
146.	                        inside = cv2.pointPolygonTest(contour[0], position, False)  
147.	                        if inside >= 0:  
148.	                            bgr += img[y][x]  
149.	                            count += 1  
150.	  
151.	                bgr /= count  
152.	                print("Pixels: ", count)  
153.	  
154.	                if show_count is True:  
155.	                    show_count = False  
156.	                elif bgr[0] != 255.0 and bgr[1] != 255.0 and bgr[2] != 255.0:  
157.	                    rgb["B"].append(bgr[0])  
158.	                    rgb["G"].append(bgr[1])  
159.	                    rgb["R"].append(bgr[2])  
160.	                    rgb['pixels'].append(count)  
161.	                    print("End the %s second(s): RGB(%s, %s, %s)" % (seconds, bgr[2], bgr[1], bgr[0]))  
162.	                    seconds += 1  
163.	  
164.	  
165.	        w = 0  
166.	        h = 0  
167.	        if draw_img is not None:  
168.	            w = draw_img.shape[1]  
169.	            h = draw_img.shape[0]  
170.	            show_img = draw_img[y0 : y0 + height, x0 : x0 + width]  
171.	            cv2.imshow(window, show_img)  
172.	        elif img is not None:  
173.	            w = img.shape[1]  
174.	            h = img.shape[0]  
175.	            show_img = img[y0 : y0 + height, x0 : x0 + width]  
176.	            cv2.imshow(window, show_img)  
177.	  
178.	        key = cv2.waitKey(25)  
179.	        if key & 0xFF == ord('r') or key & 0xFF == ord('R'):  
180.	            start = True  
181.	  
182.	        if key & 0xFF == ord('q'):  
183.	            break  
184.	  
185.	        speed = 20  
186.	        if key & 0xFF == ord('w') or key & 0xFF == ord('W'):  
187.	            y0 -= speed  
188.	  
189.	        if (key & 0xFF == ord('s') or key & 0xFF == ord('S')) and (y0 + height < h):  
190.	            y0 += speed  
191.	  
192.	        if height == h or y0 < 0:  
193.	            y0 = 0  
194.	  
195.	        if key & 0xFF == ord('a') or key & 0xFF == ord('A'):  
196.	            x0 -= speed  
197.	  
198.	        if (key & 0xFF == ord('d') or key & 0xFF == ord('D')) and (x0 + width < w):  
199.	            x0 += speed  
200.	  
201.	        if width == w or x0 < 0:  
202.	            x0 = 0  
203.	  
204.	    cv2.destroyAllWindows()  
