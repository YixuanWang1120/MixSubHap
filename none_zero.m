clc;
clear all;
w1=cell2mat(struct2cell(load('F:\\FILE\\file\\numlib\\ws0.mat')));
ww=cell2mat(struct2cell(load('F:\\FILE\\file\\numlib              \\ww.mat')));
a=find(any(w1~=0, 2));
w1 (all(w1== 0, 2),:) = [];
w1 (:,all(w1 == 0, 1)) = [];
for i=1:length(w1)
    for j=1:length(w1)
      w1(i,j)= ww(a(i),a(j))*10;
    end
end
save('F:\\FILE\\file\\numlib\\ws0_nonezero.mat', 'w1');
save('F:\\FILE\\file\\numlib\\a0.mat', 'a');
aa=find(any(ww~=0, 2));
ww (all(ww== 0, 2),:) = [];
ww (:,all(ww == 0, 1)) = [];
save('F:\\FILE\\file\\numlib\\ww_nonezero.mat', 'ww');
save('F:\\FILE\\file\\numlib\\aww.mat', 'aa');
