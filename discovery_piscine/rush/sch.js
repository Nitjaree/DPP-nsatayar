// ข้อมูลหลักสูตรเต็มรูปแบบ
const curriculaData = {
    "physics": {
        name: "วิทยาศาสตรบัณฑิต สาขาวิชาฟิสิกส์อุตสาหกรรม (หลักสูตรปรับปรุง พ.ศ. 2569)",
        faculty: "คณะวิทยาศาสตร์",
        totalCredits: 122,
        
        courses: [
            // ปี 1 เทอม 1
            { year: 1, sem: 1, code: "05016201", name: "แคลคูลัส 1", credits: 3 },
            { year: 1, sem: 1, code: "05106030", name: "เคมีทั่วไป", credits: 3 },
            { year: 1, sem: 1, code: "05106042", name: "ปฏิบัติการเคมีทั่วไป", credits: 1 },
            { year: 1, sem: 1, code: "05366001", name: "ฟิสิกส์และการประยุกต์ 1", credits: 3 },
            { year: 1, sem: 1, code: "05366005", name: "ปฏิบัติการฟิสิกส์และการประยุกต์ 1", credits: 1 },
            { year: 1, sem: 1, code: "05366022", name: "การเขียนโปรแกรมคอมพิวเตอร์", credits: 3 },
            { year: 1, sem: 1, code: "90641008", name: "พื้นฐานทักษะการสื่อสารภาษาอังกฤษ", credits: 0 },
            { year: 1, sem: 1, code: "90642036", name: "เตรียมความพร้อมสำหรับวิศวกร", credits: 1 },
            
            // ปี 1 เทอม 2
            { year: 1, sem: 2, code: "05016202", name: "แคลคูลัส 2", credits: 3 },
            { year: 1, sem: 2, code: "05366003", name: "ฟิสิกส์และการประยุกต์ 2", credits: 3 },
            { year: 1, sem: 2, code: "05366006", name: "ปฏิบัติการฟิสิกส์และการประยุกต์ 2", credits: 1 },
            { year: 1, sem: 2, code: "05366121", name: "ทฤษฎีวงจรไฟฟ้าและอิเล็กทรอนิกส์พื้นฐาน", credits: 3 },
            { year: 1, sem: 2, code: "05366024", name: "ปฏิบัติการอิเล็กทรอนิกส์", credits: 1 },
            { year: 1, sem: 2, code: "05366143", name: "การเขียนแบบวิศวกรรม", credits: 1 },
            { year: 1, sem: 2, code: "90641007", name: "พลเมืองดิจิทัล", credits: 3 },
            { year: 1, sem: 2, code: "90641004", name: "โครงงานกลุ่ม 1", credits: 1 },

            // ปี 2 เทอม 1
            { year: 2, sem: 1, code: "05366038", name: "สถิติในงานอุตสาหกรรม", credits: 3 },
            { year: 2, sem: 1, code: "05366020", name: "คณิตศาสตร์สำหรับนักฟิสิกส์", credits: 3 },
            { year: 2, sem: 1, code: "05366025", name: "อิเล็กทรอนิกส์ดิจิตอล", credits: 3 },
            { year: 2, sem: 1, code: "05366027", name: "ปฏิบัติการอิเล็กทรอนิกส์ดิจิตอล", credits: 1 },
            { year: 2, sem: 1, code: "05366028", name: "กลศาสตร์", credits: 3 },
            { year: 2, sem: 1, code: "05366039", name: "ปฏิบัติการฟิสิกส์ระดับกลาง 1", credits: 1 },
            { year: 2, sem: 1, code: "90641009", name: "ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 1", credits: 3 },

            // ปี 2 เทอม 2
            { year: 2, sem: 2, code: "05366123", name: "วงจรอิเล็กทรอนิกส์", credits: 3 },
            { year: 2, sem: 2, code: "05366030", name: "ฟิสิกส์ยุคใหม่", credits: 3 },
            { year: 2, sem: 2, code: "05366033", name: "คลื่นและทัศนศาสตร์", credits: 3 },
            { year: 2, sem: 2, code: "05366034", name: "เซ็นเซอร์และทรานสดิวเซอร์", credits: 3 },
            { year: 2, sem: 2, code: "05366040", name: "ปฏิบัติการฟิสิกส์ระดับกลาง 2", credits: 1 },
            { year: 2, sem: 2, code: "90641005", name: "โครงงานกลุ่ม 2", credits: 1 },
            { year: 2, sem: 2, code: "05356100", name: "วิชาเลือก (กลุ่มฟิสิกส์)", credits: 3 }
        ],

    },
    "iot": {
        name: "วิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมระบบไอโอทีและสารสนเทศ (หลักสูตรปรับปรุง พ.ศ. 2569)",
        faculty: "คณะวิศวกรรมศาสตร์",
        totalCredits: 138,
        
        courses: [  
            // ปี 1 เทอม 1
            { year: 1, sem: 1, code: "01006030", name: "แคลคูลัส 1", credits: 3 },
            { year: 1, sem: 1, code: "01006020", name: "ฟิสิกส์ทั่วไป 1", credits: 3 },
            { year: 1, sem: 1, code: "01006021", name: "ปฏิบัติการฟิสิกส์ทั่วไป 1", credits: 1 },
            { year: 1, sem: 1, code: "01006012", name: "การเขียนโปรแกรมคอมพิวเตอร์", credits: 3 },
            { year: 1, sem: 1, code: "01236604", name: "วงจรไฟฟ้าและอิเล็กทรอนิกส์", credits: 3 },
            { year: 1, sem: 1, code: "01236605", name: "ปฏิบัติการวงจรไฟฟ้าและอิเล็กทรอนิกส์", credits: 1 },
            { year: 1, sem: 1, code: "90641008", name: "พื้นฐานทักษะการสื่อสารภาษาอังกฤษ", credits: 0 },
            { year: 1, sem: 1, code: "90642036", name: "เตรียมความพร้อมสำหรับวิศวกร", credits: 1 },

            // ปี 1 เทอม 2
            { year: 1, sem: 2, code: "01006031", name: "แคลคูลัส 2", credits: 3 },
            { year: 1, sem: 2, code: "01006022", name: "ฟิสิกส์ทั่วไป 2", credits: 3 },
            { year: 1, sem: 2, code: "01006023", name: "ปฏิบัติการฟิสิกส์ทั่วไป 2", credits: 1 },
            { year: 1, sem: 2, code: "01236610", name: "ปฏิบัติการเขียนแบบสามมิติทางวิศวกรรม", credits: 1 },
            { year: 1, sem: 2, code: "01236603", name: "พื้นฐานการออกแบบระบบดิจิทัล", credits: 3 },
            { year: 1, sem: 2, code: "01236609", name: "ปฏิบัติการออกแบบระบบดิจิทัล", credits: 1 },
            { year: 1, sem: 2, code: "90641007", name: "พลเมืองดิจิทัล", credits: 3 },
            { year: 1, sem: 2, code: "90641004", name: "โครงงานกลุ่ม 1", credits: 1 },
            { year: 1, sem: 2, code: "90642118", name: "โปรแกรมคอมพิวเตอร์ประยุกต์ทางธุรกิจ", credits: 2 },

            // ปี 2 เทอม 1
            { year: 2, sem: 1, code: "01236601", name: "ความน่าจะเป็นและสถิติ", credits: 3 },
            { year: 2, sem: 1, code: "01236602", name: "คณิตศาสตร์ดิสครีต", credits: 3 },
            { year: 2, sem: 1, code: "01236611", name: "พื้นฐานระบบไอโอที", credits: 3 },
            { year: 2, sem: 1, code: "01236613", name: "การเขียนโปรแกรมเชิงวัตถุ", credits: 3 },
            { year: 2, sem: 1, code: "01236619", name: "การออกแบบเชิงปฏิสัมพันธ์", credits: 3 },
            { year: 2, sem: 1, code: "90641009", name: "ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 1", credits: 3 },

            // ปี 2 เทอม 2
            { year: 2, sem: 2, code: "01236600", name: "พีชคณิตเชิงเส้นและสมการเชิงอนุพันธ์", credits: 3 },
            { year: 2, sem: 2, code: "01236615", name: "หลักการระบบการสื่อสาร", credits: 3 },
            { year: 2, sem: 2, code: "01236626", name: "การวิเคราะห์และออกแบบระบบ", credits: 3 },
            { year: 2, sem: 2, code: "01236614", name: "โครงสร้างข้อมูลและอัลกอริทึม", credits: 3 },
            { year: 2, sem: 2, code: "01236616", name: "การสื่อสารข้อมูลและเครือข่ายในระบบไอโอที", credits: 3 },
            { year: 2, sem: 2, code: "90641005", name: "โครงงานกลุ่ม 2", credits: 1 }
        ],

    },
    "comiot": {
        name: "วิศวกรรมศาสตรบัณฑิต สาขาวิชาวิศวกรรมคอมพิวเตอร์และไอโอที (ต่อเนื่อง) (หลักสูตรปรับปรุง พ.ศ. 2569)",
        faculty: "คณะวิศวกรรมศาสตร์",
        totalCredits: 118,
        courses: [
            // ปี 1 เทอม 1
            { year: 1, sem: 1, code: "01446001", name: "แคลคูลัสสำหรับวิศวกรรมคอมพิวเตอร์", credits: 3 },
            { year: 1, sem: 1, code: "01446002", name: "คณิตศาสตร์วิศวกรรมคอมพิวเตอร์", credits: 3 },
            { year: 1, sem: 1, code: "01446003", name: "สถิติและความน่าจะเป็น", credits: 3 },
            { year: 1, sem: 1, code: "01006012", name: "การเขียนโปรแกรมคอมพิวเตอร์", credits: 3 },
            { year: 1, sem: 1, code: "90641007", name: "พลเมืองดิจิทัล", credits: 3 },
            { year: 1, sem: 1, code: "90642118", name: "โปรแกรมคอมพิวเตอร์ประยุกต์ทางธุรกิจ", credits: 2 },

            // ปี 1 เทอม 2
            { year: 1, sem: 2, code: "01446004", name: "การออกแบบระบบดิจิทัล", credits: 3 },
            { year: 1, sem: 2, code: "01446005", name: "วงจรไฟฟ้าและอิเล็กทรอนิกส์", credits: 3 },
            { year: 1, sem: 2, code: "01446006", name: "ปฏิบัติการอิเล็กทรอนิกส์และระบบดิจิทัล", credits: 1 },
            { year: 1, sem: 2, code: "01446007", name: "พื้นฐานระบบไอโอที", credits: 3 },
            { year: 1, sem: 2, code: "01446009", name: "การเขียนโปรแกรมเชิงวัตถุ", credits: 3 },
            { year: 1, sem: 2, code: "90641008", name: "พื้นฐานทักษะการสื่อสารภาษาอังกฤษ", credits: 0 },
            { year: 1, sem: 2, code: "90642036", name: "เตรียมความพร้อมสำหรับวิศวกร", credits: 1 },

            // ปี 2 เทอม 1
            { year: 2, sem: 1, code: "01446025", name: "หลักการระบบสื่อสาร", credits: 3 },
            { year: 2, sem: 1, code: "01446022", name: "สถาปัตยกรรมคอมพิวเตอร์และระบบปฏิบัติการ", credits: 3 },
            { year: 2, sem: 1, code: "01446015", name: "การออกแบบเชิงปฏิสัมพันธ์", credits: 3 },
            { year: 2, sem: 1, code: "01446024", name: "การวิเคราะห์และออกแบบระบบ", credits: 3 },
            { year: 2, sem: 1, code: "01446010", name: "โครงสร้างข้อมูลและอัลกอริทึม", credits: 3 },
            { year: 2, sem: 1, code: "90641009", name: "ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 1", credits: 3 },

            // ปี 2 เทอม 2
            { year: 2, sem: 2, code: "01446012", name: "การสื่อสารข้อมูลและเครือข่ายคอมพิวเตอร์", credits: 3 },
            { year: 2, sem: 2, code: "01446008", name: "ไมโครคอนโทรลเลอร์และระบบสมองกลฝังตัว", credits: 3 },
            { year: 2, sem: 2, code: "01446020", name: "ปฏิบัติการทางวิศวกรรมคอมพิวเตอร์และไอโอที 1", credits: 1 },
            { year: 2, sem: 2, code: "01446023", name: "การดำเนินการระบบคลาวด์เชิงปฏิบัติ", credits: 1 },
            { year: 2, sem: 2, code: "01446019", name: "เซนเซอร์และระบบไซเบอร์ทางกายภาพ", credits: 3 },
            { year: 2, sem: 2, code: "90641010", name: "ทักษะการสื่อสารภาษาอังกฤษระหว่างวัฒนธรรม 2", credits: 3 }
        ],
        

    }
};

function initSelectors() {
    const leftSelect = document.getElementById('curriculumLeft');
    const rightSelect = document.getElementById('curriculumRight');

    let optionsHtml = '';
    for (const [key, val] of Object.entries(curriculaData)) {
        optionsHtml += `<option value="${key}">${val.name}</option>`;
    }

    leftSelect.innerHTML = optionsHtml;
    rightSelect.innerHTML = optionsHtml;

    leftSelect.value = 'physics';
    rightSelect.value = 'iot';

    updateView('left');
    updateView('right');
}

function toggleMode(side) {
    const modeKey = side === 'left' ? 'modeLeft' : 'modeRight';
    const filterKey = side === 'left' ? 'termFilterLeft' : 'termFilterRight';
    
    const mode = document.getElementById(modeKey).value;
    const filterDiv = document.getElementById(filterKey);

    if (mode === 'term') {
        filterDiv.style.display = 'flex';
    } else {
        filterDiv.style.display = 'none';
    }

    updateView(side);
}

function updateView(side) {
    const selectKey = side === 'left' ? 'curriculumLeft' : 'curriculumRight';
    const modeKey = side === 'left' ? 'modeLeft' : 'modeRight';
    const yearKey = side === 'left' ? 'yearLeft' : 'yearRight';
    const semKey = side === 'left' ? 'semLeft' : 'semRight';
    const infoKey = side === 'left' ? 'infoLeft' : 'infoRight';
    const contentKey = side === 'left' ? 'contentLeft' : 'contentRight';
    const iconKey = side === 'left' ? 'iconleft' : 'iconright';

    const selectedId = document.getElementById(selectKey).value;
    const mode = document.getElementById(modeKey).value;
    const curr = curriculaData[selectedId];

    // แสดงข้อมูลสรุปหลักสูตร
    document.getElementById(infoKey).innerHTML = `
        <strong>${curr.name}</strong><br>￼
        สังกัด: ${curr.faculty} | รวม: ${curr.totalCredits} หน่วยกิต
    `;
    if (selectedId === 'physics') {
        document.getElementById(iconKey).src = './sci.png';
    } else if (selectedId === 'iot') {
        document.getElementById(iconKey).src = './eng.jpg';
    } else if (selectedId === 'comiot') {
        document.getElementById(iconKey).src = './eng.jpg';
    }

    let html = '';

    if (mode === 'all') {
        // แสดงทั้งหมดทุกเทอม
        for (let y = 1; y <= 4; y++) {
            for (let s = 1; s <= 2; s++) {
                const termCourses = curr.courses.filter(c => c.year === y && c.sem === s);
                if (termCourses.length > 0) {
                    html += `<h4>ปีที่ ${y} ภาคการศึกษาที่ ${s}</h4>`;
                    html += `<table>
                                <thead>
                                    <tr>
                                        <th style="width: 25%;">รหัสวิชา</th>
                                        <th>ชื่อวิชา</th>
                                        <th class="text-center" style="width: 15%;">นก.</th>
                                    </tr>
                                </thead>
                                <tbody>`;
                    termCourses.forEach(c => {
                        html += `<tr>
                                    <td>${c.code}</td>
                                    <td>${c.name}</td>
                                    <td class="text-center">${c.credits}</td>
                                 </tr>`;
                    });
                    html += `</tbody></table>`;
                }
            }
        }
    } else {
        // แสดงเฉพาะเทอมที่เลือก
        const selectedYear = parseInt(document.getElementById(yearKey).value);
        const selectedSem = parseInt(document.getElementById(semKey).value);
        
        const filteredCourses = curr.courses.filter(c => c.year === selectedYear && c.sem === selectedSem);

        html += `<h4>ปีที่ ${selectedYear} ภาคการศึกษาที่ ${selectedSem}</h4>`;
        
        if (filteredCourses.length > 0) {
            html += `<table>
                        <thead>
                            <tr>
                                <th style="width: 25%;">รหัสวิชา</th>
                                <th style="width: 60%;">ชื่อวิชา</th>
                                <th class="text-center" style="width: 15%;">นก.</th>
                            </tr>
                        </thead>
                        <tbody>`;
            filteredCourses.forEach(c => {
                html += `<tr>
                            <td>${c.code}</td>
                            <td>${c.name}</td>
                            <td class="text-center">${c.credits}</td>
                         </tr>`;
            });
            html += `</tbody></table>`;
        } else {
            html += `<div class="no-data">ไม่พบรายวิชาในเทอมนี้</div>`;
        }
    }

    document.getElementById(contentKey).innerHTML = html;
}

function showContact(){
    if (document.getElementById('Contact').value === "Pill"){
        window.location = "pill.html";
    } else {
        window.location = "ninja.html";
    }

}

// เริ่มต้นทำงานเมื่อโหลดหน้าเว็บ
window.onload = initSelectors;